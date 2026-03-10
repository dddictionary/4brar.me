#!/bin/bash

# Ensure we're using the correct base URL
API_BASE_URL="http://localhost:5000/api/timeline_post"

UNIQUE_SUFFIX=$(date +%s)
TEST_CONTENT="Simple test post content - $UNIQUE_SUFFIX"
TEST_EMAIL="testuser-$UNIQUE_SUFFIX@example.com"
TEST_NAME="Test User $UNIQUE_SUFFIX"

echo "Generated unique content: '$TEST_CONTENT'"
echo "Generated unique email: '$TEST_EMAIL'"
echo "Generated unique name: '$TEST_NAME'"

echo -e "\nSending POST request to create a new post..."
# Use -d multiple times for clarity, or a single string.
# Axum's Form extractor expects application/x-www-form-urlencoded.
POST_RESPONSE=$(curl -s -X POST \
    -d "name=${TEST_NAME}" \
    -d "email=${TEST_EMAIL}" \
    -d "content=${TEST_CONTENT}" \
    "$API_BASE_URL")

echo -e "\nPOST Response: $POST_RESPONSE"

# Extract ID using jq (ensure jq is installed)
POST_ID=$(echo "$POST_RESPONSE" | jq -r '.id' 2>/dev/null)

if [ -z "$POST_ID" ] || [ "$POST_ID" == "null" ]; then
    echo "ERROR: Failed to extract post ID from POST response. Response was: $POST_RESPONSE"
    exit 1
fi

echo -e "\nSuccessfully created post with ID: $POST_ID"

echo -e "\nSending GET request to retrieve all posts..."
GET_RESPONSE=$(curl -s "$API_BASE_URL")

# Echo only a portion if it's too long
echo "GET Response (first 500 chars): ${GET_RESPONSE:0:500}..."

echo -e "\nVerifying the new post in GET response..."
if echo "$GET_RESPONSE" | grep -q "$TEST_CONTENT"; then
    echo "VERIFICATION SUCCESS: Found '$TEST_CONTENT' in the GET response."
else
    echo "VERIFICATION FAILED: Could not find '$TEST_CONTENT' in the GET response."
    exit 1
fi
