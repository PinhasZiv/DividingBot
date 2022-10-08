import Constants
import Responses
import UpdateDB as sql
from telegram import *
from telegram.ext import *

updater = Updater(token=Constants.BOT_API_TOKEN, use_context=True)

dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
	buttons = [[KeyboardButton("Add Person")], [KeyboardButton("Start dividing")]]
	context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to DistriBot", reply_markup=ReplyKeyboardMarkup(buttons))
	# update.message.reply_text(
	# 	"Hello sir, Welcome to the Bot.Please write\
	# 	/help to see the commands available.")


def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/youtube - To get the youtube URL
	/linkedin - To get the LinkedIn profile URL
	/gmail - To get gmail URL
	/geeks - To get the GeeksforGeeks URL""")


def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)

def messageHandler(update: Update, context: CallbackContext):
	ret = ''

	message_text = str(update.message.text).lower()
	message_id = update.message.message_id
	message_date = int(round(update.message.date.timestamp()))
	# message_date = message_date.strftime('%Y-%m-%d %H:%M:%S')  # formatted datetime
	user = update.message.from_user
	user_id = user.id
	chat_id = update.message.chat.id
	print('update:', update)
	print('user_id:', user_id)
	print('chat_id:', chat_id)
	print('message id:', message_id)
	print('message_date', message_date)
	if not context.user_data:
		context.user_data['state'] = 0
	if not context.chat_data:
		# context.chat_data['admin'] = user_id
		context.chat_data['users_list'] = {}
	if user_id not in context.chat_data['users_list']:
		context.chat_data['users_list'][user_id] = update.message.from_user.to_dict()
	if 'expense' not in context.user_data:
		context.user_data['expense'] = {'user_id': user_id,
										'chat_id': chat_id,
										'message_id': message_id,
										'message_date': message_date}

	user_state = context.user_data['state']
	if user_state == 0:
		success = sql.getExpenseSum(message_text, context)
		if success:
			ret = 'please enter the reason for the expense'
		else:
			ret = 'please enter only integer or float'
	elif user_state == 1:
		sql.getExpenseReason(message_text, context)
		data = context.user_data['expense']
		adding = sql.addExpense(
			data['user_id'], data['chat_id'], data['message_id'], data['amount'], data['reason'], data['message_date'])
		if 'error' in adding:
			ret = 'some problem happened. please try again'
		else:
			ret = adding
			context.user_data['state'] = 0
	else:
		print('Error. range of state should be 0-1')

	# ret = Responses.sample_responses(message_text)
	print('user data:', context.user_data)
	print('chat data:', context.chat_data)
	update.message.reply_text(ret)


def new_user_added(update: Update, context: CallbackContext):
	if 'users_list' not in context.chat_data:
		context.chat_data['users_list'] = {}
	for user in update.message.new_chat_members:
		context.chat_data['users_list'][user.id] = user.to_dict()
	print(context.chat_data)

# function to remove users that left the group from users_list
def user_left(update: Update, context: CallbackContext):
	if 'users_list' not in context.chat_data:
		pass
	# remove user from user_list, if exists
	elif update.message.left_chat_member.id in context.chat_data['users_list']:
		context.chat_data['users_list'].pop(update.message.left_chat_member.id)
	print(context.chat_data)


# def addExpense():

dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user_added))
dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, user_left))
dispatcher.add_handler((MessageHandler(Filters.text, messageHandler)))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
# dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# dispatcher.add_handler(MessageHandler(
# 	Filters.command, unknown)) # Filters out unknown commands
#
# # Filters out unknown messages.
# dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
