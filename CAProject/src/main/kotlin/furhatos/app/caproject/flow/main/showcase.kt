package furhatos.app.caproject.flow.main

import furhatos.app.caproject.events.SetPicSolo
import furhatos.app.caproject.flow.Parent
import furhatos.flow.kotlin.*
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes

var CURRENT_ART = Art("default", "/fake/image.png")

enum class Sentiment {
    POSITIVE, NEGATIVE
}

var sentiment = Sentiment.POSITIVE

val Purpose : State = state(Parent) {
    onEntry {
        furhat.ask("Nice to meet you ${NAME}! Why are you looking for art?")
    }

    onResponse {
        println(it.text)
        furhat.say("Nice! I'll keep that in mind for you today!")
        Recommender.processPurpose(it.text)
        goto(Preference)
    }

}


val Preference : State = state(Parent) {
    onEntry {
        furhat.ask("Okay what kind of art are you interested in?")
    }

    onResponse {
        println(it.text)
        furhat.say("Awesome, let me find some cool art for you!")
        Recommender.processPreferences(it.text)
        goto(Showcase)
    }

}

val Showcase : State = state(Parent) {
    var art = Art("default", "/fake/image.png")
    onEntry {
        furhat.say("Here is my recommendation for you")
        art = Recommender.getArt()


        //Connection to GUI
        send(SetPicSolo(art.imagePath))
        println("send pic to gui")
        var artist=""
        var medium=""
        var timePeriod=""

        if (!art.artist.equals("")){ artist=" ${art.artist}'s" }
        if (!art.medium.equals("")){ medium=" on ${art.medium}" }
        if (!art.timePeriod.equals("")){ timePeriod=" from ${art.timePeriod}" }


        furhat.say("This is${artist} ${art.title}${medium}${timePeriod}")

        furhat.ask("What are your thoughts on the art?")
        println("finished saying")

    }
    onResponse<Yes> {
        furhat.say("It's nice that you like it")
        goto(ShowcaseMore)

    }
    onResponse{
        println(it.text)


        sentiment = Recommender.processUserResponse(art.id, it.text)
        goto(ShowcaseMore)
    }
}

val ShowcaseMore : State = state(Parent) {
    onEntry {
        furhat.ask("Would you like to explore more artworks?")
    }
    onResponse<Yes> {
        when(sentiment) {
            Sentiment.POSITIVE -> goto(ShowcaseSimilar)
            Sentiment.NEGATIVE -> goto(Preference)
        }
    }
    onResponse<No> {
        goto(Ending)
    }
}

val ShowcaseSimilar : State = state(Parent) {
    onEntry {
        furhat.ask("Would you like to see  artworks similar to the previous?")
    }
    onResponse<Yes> {
        goto(Showcase)
    }
    onResponse<No> {
        goto(Preference)
    }
}


