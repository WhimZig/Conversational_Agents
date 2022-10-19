package furhatos.app.caproject.events

import furhatos.event.Event


class LoggingGui(var param1: String? = null) : Event()
class SetPics(var pics:String? =null):Event()
class SetPicSolo(var pic:String? =null):Event()
