import rosbag

from python_qt_binding.QtGui import QGraphicsScene, QGraphicsView, QIcon
from python_qt_binding.QtCore import QSize, qWarning, qErrnoWarning

from naoqi_bridge_msgs.msg import AudioBuffer

class AudioPlayer(object):
    def __init__(self):
        self.player = None
        try:
            import ossaudiodev
            self.device = ossaudiodev.open('w')
            self.device.setfmt(ossaudiodev.AFMT_S16_LE)
            self.player = 'oss'
        except Exception, e:
            qWarning('Could not open dsp device :%s'%e)
            try:
                import alsaaudio
                self.device = alsaaudio.PCM()
                self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                self.player = 'alsa'
                qWarning('Using alsaaudio. If sound quality is not good enough, consider installing osspd')
            except Exception, e:
                raise e

        self.channels = None
        self.speed = None

    def setChannels(self, channels):
        if not self.channels or self.channels != channels:
            self.channels = channels
            if self.player == 'oss':
                self.device.channels(channels)
            elif self.player == 'alsa':
                self.device.setchannels(channels)

    def setRate(self, rate):
        if not self.speed or self.speed != rate:
            self.speed = rate
            if self.player == 'oss':
                self.device.speed(rate)
            elif self.player == 'alsa':
                self.device.setrate(rate)

    def play(self, data):
        if self.player == 'oss' or self.player == 'alsa':
            self.device.write(data)




bag = rosbag.Bag('/home/mmoreaux/rosbag/2016-02-04-14-37-41.bag')

msg = None


for topic, msg, t in bag.read_messages(topics=['/pepper_robot/audio']):
	print topic
	break


player = AudioPlayer()
player.setChannels(len(msg.channelMap))
player.setRate(msg.frequency)

for topic, msg, t in bag.read_messages(topics=['/pepper_robot/audio']):
	msgToPlay = list(msg.data)

	# play a chunk of the recorded data (very small chunk !!! :p )
	for idx in xrange(0, len(msgToPlay), 4):
		msgChunk = msgToPlay[idx : idx+4]
		dataBuff = ""

		# Turn the list of int16 into a buffer of raw data
		for i in range (0,len(msgChunk)) :
			if msgChunk[i]<0 :
				msgChunk[i]=msgChunk[i]+65536
			dataBuff = dataBuff + chr(msgChunk[i]%256)
			dataBuff = dataBuff + chr( (msgChunk[i] - (msgChunk[i]%256)) /256)

		player.play(dataBuff)

bag.close()

