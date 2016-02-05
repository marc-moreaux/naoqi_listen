# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import rospy

from rqt_bag import TopicMessageView

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




def listener():
    rospy.Subscriber("/pepper_robot/audio", String, callback)



def callback(data):
    player = AudioPlayer()


    topic, msg, t = data
        break

    player.setChannels(len(msg.channelMap))
    player.setRate(msg.frequency)

    tmp = list(msg.data)
    dataBuff = ""

    # Turn the list of int16 into a buffer of raw data
    for i in range (0,len(tmp)) :
        if tmp[i]<0 :
            tmp[i]=tmp[i]+65536
        dataBuff = dataBuff + chr(tmp[i]%256)
        dataBuff = dataBuff + chr( (tmp[i] - (tmp[i]%256)) /256)

    player.play(dataBuff)