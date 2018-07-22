from flask import Flask, render_template, request, redirect, url_for
import dataset
app = Flask(__name__)

db_url = "postgres://toummemjrmwxea:cd7c72af4761741639b72c0018fa99c5d3aafdb37916c6088fc7d54a88e25d71@ec2-174-129-206-173.compute-1.amazonaws.com:5432/dark4smob4i6hv"
db = dataset.connect(db_url)

# Stores the list of users
user_table = db.create_table('users')
# Stores the list of messages
message_table = db.create_table('messages')

@app.route('/')
def homepage():
    return redirect(url_for("show_messages"))

def show_db():
    # Use dataset to show all db contents
    all_users = list(user_table.find())
    all_messages = list(message_table.find())
    return "Users:<br>" + str(all_users) + "<br>Messages:<br>" + str(all_messages)

#############################
### Code for adding users ###
#############################

@app.route('/userForm')
def user_form():
    return render_template('user_form.jinja')

@app.route('/handleUserForm', methods=["GET","POST"])
def handle_user_form():
    print("handleUserForm()")
    # Get the name they typed in
    name = request.form["username"]
    # And call our add_user() function!
    add_user(name)

def add_user(name):
    if user_table.find_one(name=name):
        return "User already exists!"
    else:
        user_table.insert(dict(name=name))
        return "User added!"

# Show a list of all users
@app.route('/showUsers')
def show_users():
    all_user_data = user_table.find()
    all_user_names = []
    for user_data in all_user_data:
        # Get the user's name
        user_name = user_data["name"]
        all_user_names.append(user_name)
    return render_template('user_list.jinja', user_list=all_user_names)

############################################
### Code for adding and showing messages ###
############################################

# Give the visitor a message form
@app.route('/messageForm')
def message_form():
    return render_template("message_form.jinja")

# Parse the entered data and then call add_message()
@app.route('/handleMessageForm', methods=["GET","POST"])
def handle_message_form():
    # Get the text they entered in the form
    from_name = request.args.get("fromname", None)
    if not from_name:
        return "from_name None!"
    to_name = request.args.get("toname", None)
    if not to_name:
        return "to_name None!"
    message_text = request.args.get("messagetext", None)
    if not message_text:
        return "message_text None!"
    # Now just call our add_message function!
    return add_message(message_text, from_name, to_name)

# Add a message to the db
def add_message(text, sender_name, recipient_name):
    # Remember that we need to update the message table AND the links table
    if message_table.find_one(text=text):
        return "Message already exists!"
    else:
        # Find the id of the sender
        sender_data = user_table.find_one(name=sender_name)
        if sender_data:
            sender_id = sender_data["id"]
        else:
            return "Sender not found!"
        # Find the id of the recipient
        recipient_data = user_table.find_one(name=recipient_name)
        if recipient_data:
            recipient_id = recipient_data["id"]
        else:
            return "Recipient not found!"
        # Add to message table
        message_id = message_table.insert(dict(text=text, sender_id=sender_id, recipient_id=recipient_id))
        return "Message inserted!"

# Show a list of all messages
@app.route('/showMessages')
def show_messages():
    all_message_data = []
    all_messages = list(message_table.find())
    for message in all_messages:
        message_text = message["text"]
        message_sender_id = message["sender_id"]
        message_recipient_id = message["recipient_id"]
        # Let's get the sender's name
        message_sender_data = user_table.find_one(id=message_sender_id)
        message_sender_name = message_sender_data["name"]
        # And the recipient's name
        message_recipient_data = user_table.find_one(id=message_recipient_id)
        message_recipient_name = message_recipient_data["name"]
        # Add this message's data to the list of all data
        all_message_data.append(dict(text=message_text, sender_name=message_sender_name, recipient_name=message_recipient_name))
    return render_template('message_list.jinja', message_list=all_message_data)

###################################
### Code for adding sample data ###
###################################

@app.route('/setup')
def setup_easy():
    # THIS IS THE EASY WAY TO DO THE SETUP! Just use the add_message() and
    # addUser() functions we wrote above :)
    user_table.delete()
    message_table.delete()
    # Add users
    add_user("Jeff")
    add_user("Tahseen")
    add_user("Sadek")
    # Add messages
    add_message("Hello friends!", "Jeff", "Tahseen")
    add_message("I'm shutting down the camp", "Sadek", "Jeff")
    add_message("Coding is fun!", "Tahseen", "Sadek")
    return "DB set up!"

if __name__ == "__main__":
    app.run(debug=True)