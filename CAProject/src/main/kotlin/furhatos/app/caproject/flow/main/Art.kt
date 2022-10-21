package furhatos.app.caproject.flow.main

data class Art (
    val id: String,
    val imagePath: String,
    val title: String = "fake",
    val artist: String = "picasso",
    val medium: String = "oil",
    val timePeriod: String = "1500s"
)