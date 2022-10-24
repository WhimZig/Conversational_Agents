package furhatos.app.caproject.flow.main

import org.json.JSONObject
import java.util.Arrays

object Recommender {
    fun processPurpose(text: String) {
        println("processing purpose!")
        //val purpose_list = khttp.post("http://localhost:8000/nlu/purpose", data = mapOf("text" to text))

        // It's a list of one element at this point, can adjust it for more
        val purpose_list = khttp.post("http://localhost:8000/nlu/keywords", json = mapOf("text" to text))

        println("processed purpose!")
    }

    fun processPreferences(text: String) {
        println("processing preferences!")
        val feature_list =
            khttp.post("http://localhost:8000/nlu/feature", json = JSONObject(mapOf("text" to text))).jsonObject
        println(feature_list)

        khttp.post(
            "http://localhost:8000/mem/topic",
            json = JSONObject(mapOf("text" to (feature_list.get("feature1") as String)))
        )
        khttp.post(
            "http://localhost:8000/mem/topic",
            json = JSONObject(mapOf("text" to (feature_list.get("feature2") as String)))
        )
        khttp.post(
            "http://localhost:8000/mem/topic",
            json = JSONObject(mapOf("text" to (feature_list.get("feature3") as String)))
        )

        println("processed preferences!")

    }

    fun processUserResponse(artId: String, response: String): Sentiment {
        println("processing sentiment on art: $artId , response: $response")

        //Connection to gaze part / stopping gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/stop")
        val attention = khttp.get("http://localhost:8000/gaze/getAttention").jsonObject.get("attention") as Float
        val sentiment = khttp.post(
            "http://localhost:8000/nlu/sentiment",
            json = mapOf("text" to response)
        ).jsonObject.get("sentiment") as Float
        // if there is a problem here put the attribute calling somewhere after the function
        val combined_score = 0.5 * sentiment + 0.5 * attention * sentiment

        khttp.post(
            "http://localhost:8000/mem/painting_score",
            json = mapOf("text" to artId, "sentiment" to combined_score)
        )
        if (combined_score > 0) {
            return Sentiment.POSITIVE
        } else {
            return Sentiment.NEGATIVE
        }
    }

    fun getArt(): Art {
        println("getting art!")
        // TODO: connect this to Python preference engine
        //Connection to gaze part / starting gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/start")

        val art = khttp.get("http://localhost:8000/mem/painting_recommend").jsonObject
        var art1 = Art(art.get("filename") as String, art.get("filename") as String)
        art1.artist = art.get("artist") as String
        art1.title = art.get("piece_name") as String
        art1.medium = art.get("medium") as String
        art1.timePeriod = art.get("period") as String
        return art1
    }
}   