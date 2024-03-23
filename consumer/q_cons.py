from flask import Flask,jsonify, request
from jobs import *
from notify import *


from models import Letters, User




app = Flask(__name__)

@app.route('/')
def test():
    return jsonify({"status":"the consumer is up and running !"}),200
@app.route('/process',methods=["POST"])
def process_letter():
    
    # TODO next key verificaiton fails check it
   
    QSTASH_CURRENT_SIGNING_KEY = os.getenv('QSTASH_CURRENT_SIGNING_KEY') or os.environ["QSTASH_CURRENT_SIGNING_KEY"] 
    QSTASH_NEXT_SIGNING_KEY = os.getenv('QSTASH_NEXT_SIGNING_KEY') or os.environ["QSTASH_NEXT_SIGNING_KEY"] 

    

    
    task=request.get_json()
    signature = request.headers.get('Upstash-Signature')
    # print
    print(signature)
# TODO maybe validate with both keys
    valid = verify_request(current_key=QSTASH_CURRENT_SIGNING_KEY,next_key=QSTASH_NEXT_SIGNING_KEY ,url=task["url"],body=request.data,signature=signature)
    
    print("valid:",valid)
    if valid["status"]:
        print("valid")
        print("starting task..")
        # print(task)
        if task["task_name"]==Tasks.make_letter.value:
                if not task["attached"]:
                    print("ënterin")
                    Letters.Write(task)
                    
                    print( "LETTER(NO IMAGES) CREATION TASK FINISHED!! ")
            
                    return jsonify({"status":"letter created"}),200     
                else:     
                    print(f"got task:{task['letter_title']} | type:{type(task)}...started")               
                    letter_id = Letters.Write(task)
                    Letters.AddImage(image_data_list=task["image_data_list"],letter_id=letter_id)
                    print( "IMAGE ADD TASK FINISHED!! ")                        
                    return jsonify({"status":"LETTER WITH IMAGES CREATED"}),200       
            
    else:
        print("not valid: err=",valid["info"])
        return jsonify({"Error":valid["info"]}),400
  


if __name__ == "__main__":
    app.run(debug=True,port=3000)