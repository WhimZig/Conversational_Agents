package furhatos.app.caproject.flow.main

data class Art (
    val id: String,
    val imagePath: String,
    val title: String = "",
    val artist: String = "",
    val medium: String = "",
    val timePeriod: String = ""
)