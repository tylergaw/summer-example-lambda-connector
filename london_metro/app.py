import json
import requests
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(req, context):
    logger.info("Received request: %s", json.dumps(req))
    result = requests.get(
        "https://api.tfl.gov.uk/line/mode/tube/status",
        headers={"content-type": "application/json", "charset": "utf-8"},
    )

    since_id = None
    timeline = json.loads(result.text)

    tflLineStatus = []
    for t in timeline:
        # Remember the first id we encounter, which is the most recent
        if since_id == None:
            since_id = t["id"]

        # Add all tflLineStatus
        tflLineStatus.append(
            {
                "linename": t["id"],
                "status": t["lineStatuses"][0]["statusSeverityDescription"],
                "timestamp": t["created"],
            }
        )

    if since_id == None:
        since_id = req.state.since_id
    ans = {
        # Remember the most recent id, so our requests are incremental
        "state": {since_id: since_id},
        "schema": {"line_status": {"primary_key": ["linename"]}},
        "insert": {"line_status": tflLineStatus},
        "hasMore": False,
    }
    return json.dumps(ans)
