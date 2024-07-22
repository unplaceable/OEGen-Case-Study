import requests
import os


def new_pipeline_alert(pipeline_data):
    print('creating slack message')
    message = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"A new pipeline has been created!\n>Name: {pipeline_data['ProjectName']}\n>Technology: {pipeline_data['Technology']}\n>Build date: {pipeline_data['RTBDate']}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "View pipeline"
				},
				"url": f"http://localhost:8501/Pipelines?pipeline_id={pipeline_data['ID']}"
			}
		}
	]
}
    post_message(message)
    print('slack message sent')




def post_message(message):

    x = requests.post(os.environ.get('NEW_PIPELINE_SLACK_WEBHOOK', None), json = message)