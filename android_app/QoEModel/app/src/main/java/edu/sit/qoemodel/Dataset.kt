package edu.sit.qoemodel

import android.content.res.AssetManager
import java.io.File

class Dataset(
    private val assetManager: AssetManager
) {

    fun read(
        filePath: String,
        nSamples: Long,
        nTimesteps: Long,
        nFeatures: Long
    ): Pair<FloatArray, FloatArray> {
        val inputStream = assetManager.open(filePath).bufferedReader()

        var data = floatArrayOf()
        var output = floatArrayOf()

        inputStream.use {
            for (i in 0 until nSamples) {
                for (j in 0 until nTimesteps) {
                    for (k in 0 until nFeatures) {
                        data += it.readLine().toFloat()
                    }
                }
            }
        }

        for (i in 0 until nSamples) {
            for (j in 0 until 1) {
                for (k in 0 until 1) {
                    output += 0.0f
                }
            }
        }


        return Pair(data, output)
    }

    fun readMultiple(
        filePath: String,
        nSamples: Long,
        nTimesteps: Long,
        nFeatures: Long
    ): Pair<MutableList<FloatArray>, MutableList<FloatArray>> {
        var dataList = mutableListOf<FloatArray>()
        var outputList = mutableListOf<FloatArray>()

        val inputStream = assetManager.open(filePath).bufferedReader()
        inputStream.use {
            for (i in 0 until nSamples) {
                var data = floatArrayOf()

                for (j in 0 until nTimesteps) {
                    for (k in 0 until nFeatures) {
                        data += it.readLine().toFloat()
                    }
                }

                dataList.add(data)
            }
        }

        for (i in 0 until nSamples) {
            var output = floatArrayOf()
            for (j in 0 until 1) {
                for (k in 0 until 1) {
                    output += 0.0f
                }
            }
            outputList.add(output)
        }


        return Pair(dataList, outputList)
    }

    fun write(filePath: String, data: FloatArray) {
        println(filePath)
        val file = File(filePath).printWriter().use { out ->
            data.forEach {
                out.println(it)
            }
        }
    }

    fun write(filePath: String, data: MutableList<FloatArray>) {
        println(filePath)
        val file = File(filePath).printWriter().use { out ->
            data.forEach {
                out.println(it[0])
            }
        }
    }
}
