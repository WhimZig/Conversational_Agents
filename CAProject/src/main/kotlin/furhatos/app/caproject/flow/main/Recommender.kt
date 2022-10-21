package furhatos.app.caproject.flow.main

object Recommender {
    fun processPurpose(text: String) {
        println("processing preferences!")
        val r = khttp.post("http://localhost:8000/purpose", data = mapOf("text" to text))
        println("processed preferences!")
    }
    fun processPreferences(text: String) {
        println("processing preferences!")
        // TODO: connect this to Python preference engine
    }

    fun processUserResponse(artId: String, response: String) : Sentiment {
        println("processing sentiment on art: $artId , response: $response")
        // TODO: connect this to Python preference engine
        return Sentiment.POSITIVE
    }

    fun getArt() : Art {
        println("getting art!")
        // TODO: connect this to Python preference engine
        return Art("coolart1", "/cool/art/image.png")
    }
}   