#!/bin/bash
set -euo pipefail

# Webhook URLs
WEBHOOK_CODING_DEV="https://default863aae132f114f3ba1130e491f5868.3e.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/1beb72fbea834ef4a69a94f1796b2f65/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=LsjGxMfdIhRIVJldmVbP5ylVT4FR1vtUqsMNdlY8q-w"
WEBHOOK_DEV_TEST="https://default863aae132f114f3ba1130e491f5868.3e.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/d39e977cff5f4a2cbfc6585a916a0c33/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vfbBZo4q96wqT7J1et-CmJpUYzwItIJxABhZJNOWhZQ"

# Resolve tasks file and webhook from args
# Usage: report_to_teams.sh [tasks_file_or_webhook] [webhook]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_FILE="${SCRIPT_DIR}/../data/tasks.json"
WEBHOOK_KEY="coding-dev"

# Parse args: first arg could be tasks file or webhook key
if [ $# -ge 1 ]; then
    if [ -f "$1" ]; then
        TASKS_FILE="$1"
        if [ $# -ge 2 ]; then
            WEBHOOK_KEY="$2"
        fi
    else
        WEBHOOK_KEY="$1"
    fi
fi

# Select webhook URL
if [ "$WEBHOOK_KEY" = "dev-test" ]; then
    WEBHOOK_URL="$WEBHOOK_DEV_TEST"
else
    WEBHOOK_URL="$WEBHOOK_CODING_DEV"
fi

# Check if tasks file exists
if [ ! -f "$TASKS_FILE" ]; then
    echo "No tasks file found"
    exit 0
fi

# Pre-filter tasks (keeps the loop in the parent shell so TASK_BLOCKS updates propagate)
TASK_LINES=$(jq -c '.[] | select(.status == "done" or .status == "progress")' "$TASKS_FILE")

# Build task blocks for Adaptive Card
TASK_BLOCKS="[]"

# Read tasks and filter by status (done or progress)
while IFS= read -r task; do
    status=$(echo "$task" | jq -r '.status')

    # Extract task details
    task_id=$(echo "$task" | jq -r '.id // ""')
    title=$(echo "$task" | jq -r '.title')
    description=$(echo "$task" | jq -r '.description // "No description provided."')
    priority=$(echo "$task" | jq -r '.priority // "medium"')
    assignee=$(echo "$task" | jq -r '.assignee // ""')
    project_type=$(echo "$task" | jq -r '.project_type // ""')

    # Build title prefix as [#id] Title
    if [ -n "$task_id" ]; then
        formatted_title="[#${task_id}] $title"
    else
        formatted_title="$title"
    fi

    # Status icon and color
    if [ "$status" = "progress" ]; then
        status_icon="https://cdn-icons-png.flaticon.com/512/833/833602.png"
        title_color="Accent"
    else
        status_icon="https://cdn-icons-png.flaticon.com/512/190/190411.png"
        title_color="Good"
    fi

    # Build task block JSON via jq (auto-escapes user-controlled strings; immune to shell injection)
    task_block=$(jq -n \
      --arg status_icon "$status_icon" \
      --arg title_color "$title_color" \
      --arg title "$formatted_title" \
      --arg description "$description" \
      '{
        type: "ColumnSet",
        spacing: "Medium",
        separator: true,
        columns: [
          {
            type: "Column",
            width: "auto",
            verticalContentAlignment: "Center",
            items: [
              { type: "Image", url: $status_icon, width: "24px" }
            ]
          },
          {
            type: "Column",
            width: "stretch",
            items: [
              { type: "TextBlock", text: $title, size: "Medium", weight: "Bolder", color: $title_color, wrap: true },
              { type: "TextBlock", text: $description, isSubtle: true, size: "Small", wrap: true, spacing: "None" }
            ]
          }
        ]
      }')

    # Append to task blocks array
    TASK_BLOCKS=$(echo "$TASK_BLOCKS" | jq ". += [$task_block]")
done <<< "$TASK_LINES"

# If no tasks, add empty message
if [ "$(echo "$TASK_BLOCKS" | jq 'length')" -eq 0 ]; then
    TASK_BLOCKS=$(cat <<'EOF'
[{
  "type": "TextBlock",
  "text": "No tasks were completed today. 💤",
  "color": "warning",
  "weight": "Bolder"
}]
EOF
)
fi

# Build full Adaptive Card payload
PAYLOAD=$(cat <<EOF
{
  "type": "message",
  "attachments": [{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "\$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
      "type": "AdaptiveCard",
      "version": "1.4",
      "body": [
        {
          "type": "ColumnSet",
          "style": "emphasis",
          "columns": [
            {
              "type": "Column",
              "width": "auto",
              "items": [
                {
                  "type": "Image",
                  "url": "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/godot.png",
                  "width": "40px"
                }
              ]
            },
            {
              "type": "Column",
              "width": "stretch",
              "verticalContentAlignment": "Center",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "ADT Report : Tekton Dash",
                  "weight": "Bolder",
                  "size": "Large",
                  "color": "Accent"
                },
                {
                  "type": "TextBlock",
                  "text": "$(date +"%B %d, %Y")",
                  "isSubtle": true,
                  "size": "Small",
                  "spacing": "None"
                }
              ]
            }
          ]
        }
      ]
    }
  }]
}
EOF
)

# Merge task blocks into body
PAYLOAD=$(echo "$PAYLOAD" | jq --argjson blocks "$TASK_BLOCKS" '.attachments[0].content.body += $blocks')

# Add action button
PAYLOAD=$(echo "$PAYLOAD" | jq '.attachments[0].content.body += [{
  "type": "ActionSet",
  "actions": [{
    "type": "Action.OpenUrl",
    "title": "Open Talaria Board",
    "url": "https://dev.klud.top/talaria/",
    "style": "positive"
  }]
}]')

# Send to Teams webhook
http_code=$(curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  -s -o /dev/null -w "%{http_code}")
echo "HTTP $http_code"
if [[ "$http_code" != 2* ]]; then
    echo "Teams webhook returned $http_code" >&2
    exit 1
fi
echo "Report sent to Teams"
