import pytest
import pickle
from wee_slack import EventRouter, ProcessNotImplemented, SlackRequest

def test_EventRouter(mock_weechat):
    # Sending valid json adds to the queue.
    e = EventRouter()
    e.receive_json('{}')
    assert len(e.queue) == 1

    # Handling an event removes from the queue.
    e = EventRouter()
    # Create a function to test we are called
    e.proc['testfunc'] = lambda x, y: x
    e.receive_json('{"type": "testfunc"}')
    e.handle_next()
    assert len(e.queue) == 0

    # Handling a local event removes from the queue.
    e = EventRouter()
    # Create a function to test we are called
    e.proc['local_testfunc'] = lambda x, y: x
    e.receive_json('{"type": "local_testfunc"}')
    e.handle_next()
    assert len(e.queue) == 0

    # Handling an event without an associated processor
    # raises an exception.
    e = EventRouter()
    # Create a function to test we are called
    e.receive_json('{"type": "testfunc"}')
    with pytest.raises(ProcessNotImplemented):
        e.handle_next()

def test_EventRouterReceivedata(mock_weechat):

    e = EventRouter()
    pickled_data = pickle.dumps(SlackRequest('xoxoxoxox', "rtm.startold", {"meh": "blah"}))
    e.receive_httprequest_callback(pickled_data, 1, -1, ' {"JSON": "MEH", ', 4)
    #print len(e.reply_buffer)
    e.receive_httprequest_callback(pickled_data, 1, -1, ' "JSON2": "MEH", ', 4)
    #print len(e.reply_buffer)
    e.receive_httprequest_callback(pickled_data, 1, 0, ' "JSON3": "MEH"}', 4)
    #print len(e.reply_buffer)
    try:
        e.handle_next()
    except:
        pass

    pickled_data = pickle.dumps(SlackRequest('xoxoxoxox', "rtm.start", {"meh": "blah"}))
    rtmstartdata = open('_pytest/data/http/rtm.start.json', 'r').read()
    e.receive_httprequest_callback(pickled_data, 1, 0, rtmstartdata[:5000], 4)
    e.receive_httprequest_callback(pickled_data, 1, 0, rtmstartdata[5000:], 4)
    e.handle_next()

    #print len(e.reply_buffer)

    #print e.teams

    for t in e.teams:
        #print vars(e.teams[t])
        for c in e.teams[t].channels:
            pass
            #print c
        for u in e.teams[t].users:
            pass
            #print vars(u)


#    e = EventRouter()
#    # Create a function to test we are called
#    e.receive_json('{"type": "message"}')
#    e.handle_next()
#    assert False

    #assert False
