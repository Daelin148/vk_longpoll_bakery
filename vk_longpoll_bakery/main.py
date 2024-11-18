from dotenv import load_dotenv
import vk_api
import os
from db import RedisSingleton
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.vk_api import VkApiMethod
from states import StateMachine
from models import Session
from load_db import load_test_data
from sqlalchemy.orm import Session as Sess


load_test_data()

load_dotenv()
VK_LONPOLL_API_TOKEN = os.getenv('VK_LONPOLL_API_TOKEN')


def send_message(
    vk: VkApiMethod,
    user_id: int,
    user_msg: str,
    state,
    session: Sess
):
    message = state.get_message(user_msg, session)
    keyboard = state.get_keyboard(user_msg, session)
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard.get_keyboard()
    )


vk_session = vk_api.VkApi(token=VK_LONPOLL_API_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
redis_conn = RedisSingleton.get_connection()
statemachine = StateMachine(redis_conn=redis_conn)

for event in longpoll.listen():
    with Session() as session:
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_user and event.to_me:
                if statemachine.user_id is None:
                    statemachine.set_user(user_id=event.user_id)
                state = statemachine.get_current_state()
                msg = event.text.lower()
                id = event.user_id
                send_message(vk, id, msg, state, session)
                if msg != 'главное меню' and msg in state.get_commands(
                    msg, session
                ):
                    if (next_state := state.NEXT_STATE) is not None:
                        statemachine.set_state(next_state)
                elif msg == 'главное меню':
                    statemachine.clear()
                #     resend_message(vk, id, msg, statemachine, session)
                # elif msg == 'главное меню':
                #     statemachine.clear()
                #     resend_message(vk, id, msg, statemachine, session)
                # elif msg == 'назад':
                #     if (prev_state := state.PREVIOUS_STATE) is not None:
                #         statemachine.set_state(prev_state)
                #         resend_message(vk, id, msg, statemachine, session)
                # else:
                #     send_message(vk, id, msg, statemachine, session)
