package furhatos.app.caproject.flow

import furhatos.app.caproject.flow.main.Idle
import furhatos.app.caproject.setting.distanceToEngage
import furhatos.app.caproject.setting.maxNumberOfUsers
import furhatos.flow.kotlin.*
import furhatos.flow.kotlin.voice.Voice

val Init : State = state() {


    init {
        /** Set our default interaction parameters */
        users.setSimpleEngagementPolicy(distanceToEngage, maxNumberOfUsers)
        furhat.voice = Voice("Matthew")
        /** start the interaction */
        goto(Idle)
    }



}
