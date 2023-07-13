from flask import Flask, request

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def receive():
	json_data = request.get_json()
	print(json_data)
	return json_data

if __name__ == '__main__':
	app.run()

