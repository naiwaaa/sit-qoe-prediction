package edu.sit.qoemodel

import android.os.Bundle
import android.os.Environment
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import edu.sit.qoemodel.models.CnnModel
import edu.sit.qoemodel.models.LstmModel
import java.io.File

class MainActivity : AppCompatActivity() {
    lateinit var dataset: Dataset
    lateinit var outputDirectory: File

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        dataset = Dataset(assets)
        outputDirectory = File(getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "QoEModel")
        outputDirectory.mkdirs()
    }

    fun onCnnPredictButtonPressed(view: View) { //8020
        val txtFile = "testX_1_1140_8_4.txt"
        val pbFile = "model_1.pb"

        val numbers = "\\d+".toRegex().findAll(txtFile).map { it.value }.toList()
        val id = numbers[0]
        val nSamples = numbers[1].toLong()
        val nTimesteps = numbers[2].toLong()
        val nFeatures = numbers[3].toLong()

        val (X, y) = dataset.read("cnn/txt/$txtFile", nSamples, nTimesteps, nFeatures)
        val cnnModel = CnnModel(assets, "cnn/model/$pbFile")

        val (_, elapsedTime) = cnnModel.predict(X, y, nSamples, nTimesteps, nFeatures)

        dataset.write(
            outputDirectory.absolutePath + "/output_$id.txt",
            y
        )
    }
//    fun onCnnPredictButtonPressed(view: View) { time elapsed
//        val txtFile = "testX_0_127_8_4.txt"
//        val pbFile = "model_0.pb"
//
//        val numbers = "\\d+".toRegex().findAll(txtFile).map { it.value }.toList()
//        val id = numbers[0]
//        val nSamples = 1L //numbers[1].toLong()
//        val nTimesteps = numbers[2].toLong()
//        val nFeatures = numbers[3].toLong()
//
//        val (X, y) = dataset.read("cnn/txt/$txtFile", nSamples, nTimesteps, nFeatures)
//        val cnnModel = CnnModel(assets, "cnn/model/$pbFile")
//
//        val elapsedTimes = mutableListOf<Long>()
//        for (i in 0..10000) {
//            val (_, elapsedTime) = cnnModel.predict(X, y, nSamples, nTimesteps, nFeatures)
//            elapsedTimes += elapsedTime
////            Log.d("MainActivity", "Output $y")
//        }
//
//        val elapsedTimeMean = elapsedTimes.average()
//        Log.d("MainActivity", "Time elapsed mean: $elapsedTimeMean")
//
//        dataset.write(
//            outputDirectory.absolutePath + "/output_$id.txt",
//            y
//        )
//    }

    fun onLstmPredictButtonPressed(view: View) {
        val txtFiles = listOf(
            "testX_1_134_1_3.txt",
            "testX_15_162_1_3.txt",
            "testX_2_128_1_3.txt",
            "testX_23_123_1_3.txt",
            "testX_3_140_1_3.txt",
            "testX_5_156_1_3.txt",
            "testX_8_126_1_3.txt"
        )
        val pbFile = "model_8020.pb"
        txtFiles.forEach { txtFile ->
            val numbers = "\\d+".toRegex().findAll(txtFile).map { it.value }.toList()
            val id = numbers[0]
            val nSamples = numbers[1].toLong()
            val nTimesteps = numbers[2].toLong()
            val nFeatures = numbers[3].toLong()

            val (X, y) = dataset.readMultiple("lstm/txt/$txtFile", nSamples, nTimesteps, nFeatures)
            val cnnModel = LstmModel(assets, "lstm/model/$pbFile")
//
//            val elapsedTimes = mutableListOf<Long>()
//            for (i in 0..10000) {
            for (i in 0 until nSamples.toInt()) {
                print(X[i])
                val (_, elapsedTime) = cnnModel.predict(X[i], y[i], 1, nTimesteps, nFeatures)
            }
//                elapsedTimes += elapsedTime
//                Log.d("MainActivity", "Output $y")
//            }

//            val elapsedTimeMean = elapsedTimes.average()
//            Log.d("MainActivity", "Time elapsed mean: $elapsedTimeMean")

            dataset.write(
                outputDirectory.absolutePath + "/output_$id.txt",
                y
            )
        }
    }
//    fun onCnnPredictButtonPressed(view: View) {
//        val txtList = assets.list("cnn/txt")
//        val pbList = assets.list("cnn/model")
//
//        txtList!!.indices.forEach { i ->
//            val txtFile = txtList[i]
//            val pbFile = pbList!![i]
//
//            val numbers = "\\d+".toRegex().findAll(txtFile).map { it.value }.toList()
//            val id = numbers[0]
//            val nSamples = numbers[1].toLong()
//            val nTimesteps = numbers[2].toLong()
//            val nFeatures = numbers[3].toLong()
//
//            val (X, y) = dataset.read("cnn/txt/$txtFile", nSamples, nTimesteps, nFeatures)
//            val cnnModel = CnnModel(assets, "cnn/model/$pbFile")
//
//            val (_, elapsedTime) = cnnModel.predict(X, y, nSamples, nTimesteps, nFeatures)
//
//            dataset.write(
//                outputDirectory.absolutePath + "/output_$id.txt",
//                y
//            )
//
//            Toast.makeText(this, "Time: $elapsedTime", Toast.LENGTH_LONG).show()
//        }
//    }
}
