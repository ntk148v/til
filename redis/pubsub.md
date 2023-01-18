# Redis Pub/Sub

![](https://storage.googleapis.com/blog-images-backup/0*IKcBixNW6c66H6o4)

- Pub/Sub is buffer-like structure, allowing publishers to create content as fast as they can, and subscribers to pull content at their own pace.
- Pub/Sub works under the premise of “fire and forget”. This essentially means that every published message will be delivered to as many subscribers as there are then it will be lost from the buffer
- All messages will be delivered to all subscribers (_fan-out_). Mind you, you can have subscribers listening for different channels, which would prevent this from happening. But if you have more than one subscriber on the same channel, then all of them would get the same message. It would be up to them then, to decide what to do about that.
- There is no ACK message. Some communication protocols deal with an acknowledge message, in order for the subscribers to let the publisher know the message was received. In this case, there is nothing like that, so if your subscriber gets the message and then crashes, that data will be lost for good
