package edu.sit.qoemodel.models

import android.content.res.AssetManager
import android.os.SystemClock
import org.tensorflow.contrib.android.TensorFlowInferenceInterface

class LstmModel(assetManager: AssetManager, modelPath: String) {
    private val TAG = "LstmModel"

    private val INPUT_NAME = "lstm_input"
    private val OUTPUT_NAME = "distrib/transpose_1"

    private lateinit var mInferencer: TensorFlowInferenceInterface

    init {
        mInferencer = TensorFlowInferenceInterface(assetManager, modelPath)
        printGraph()
    }

    private fun printGraph() {
        val graph = mInferencer.graph()
        graph.operations().forEach {
            println(it.name())
        }
    }

    fun close() {
        mInferencer.close()
    }

    fun predict(
        testX: FloatArray,
        y: FloatArray,
        nSamples: Long,
        nTimesteps: Long,
        nFeatures: Long
    ): Pair<FloatArray, Long> {
        val startTime = SystemClock.uptimeMillis()

        for (n in 0 until nSamples) {
            mInferencer.feed(
                INPUT_NAME,
                testX,
                nSamples,
                nTimesteps,
                nFeatures
            )
            mInferencer.run(arrayOf(OUTPUT_NAME))
            mInferencer.fetch(OUTPUT_NAME, y)
        }
        val timeElapsed = SystemClock.uptimeMillis() - startTime
//        Log.d(TAG, "Output: $y")
//        Log.d(TAG, "Time cost to run model inference: $timeElapsed")

        return Pair(y, timeElapsed)
    }
}
