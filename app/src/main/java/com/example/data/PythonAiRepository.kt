package com.example.data

import android.content.Context
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import com.example.model.AiResponse
import com.example.model.ClosestGuess
import com.example.model.KnowledgeEntry
import com.example.model.KnowledgeStats
import com.example.model.VaultRecord
import com.example.model.VaultStatus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

data class GatherTopicResult(
    val success: Boolean,
    val title: String = "",
    val category: String = "",
    val answer: String = "",
    val sourceLabel: String = "",
    val error: String? = null,
    val stats: KnowledgeStats = KnowledgeStats(),
)

data class GatherPackResult(
    val success: Boolean,
    val savedCount: Int = 0,
    val totalCount: Int = 0,
    val error: String? = null,
    val stats: KnowledgeStats = KnowledgeStats(),
)

class PythonAiRepository(context: Context) {

    private val appContext: Context = context.applicationContext

    private fun getBridgeModule(): PyObject {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(appContext))
        }
        return Python.getInstance().getModule("android_bridge")
    }

    suspend fun initialize(): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val filesDir = appContext.filesDir.absolutePath
        val jsonStr = bridge.callAttr("init_brain", filesDir).toString()
        val obj = JSONObject(jsonStr)
        parseStats(obj.getJSONObject("stats"))
    }

    suspend fun ask(query: String, allowOnlineFetch: Boolean): AiResponse = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("ask", query, allowOnlineFetch).toString()
        val obj = JSONObject(jsonStr)
        val closestObj = if (obj.isNull("closest_guess")) null else obj.optJSONObject("closest_guess")
        val closestGuess = closestObj?.let {
            ClosestGuess(
                id = it.getInt("id"),
                question = it.getString("question"),
                answer = it.getString("answer"),
                category = it.optString("category", "General"),
                confidence = it.optDouble("confidence", 0.0),
            )
        }
        AiResponse(
            answer = obj.optString("answer", ""),
            confidence = obj.optDouble("confidence", 0.0),
            route = obj.optString("route", "knowledge"),
            category = obj.optString("category", "General"),
            matchedId = if (obj.isNull("matched_id")) null else obj.optInt("matched_id"),
            matchedQuestion = if (obj.isNull("matched_question")) null else obj.optString("matched_question"),
            needsTeaching = obj.optBoolean("needs_teaching", false),
            closestGuess = closestGuess,
            formulaSteps = obj.optString("formula_steps", ""),
            tag = obj.optString("tag", ""),
        )
    }

    suspend fun gatherTopicOnline(topic: String): GatherTopicResult = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("gather_topic", topic).toString()
        val obj = JSONObject(jsonStr)
        val stats = parseStats(obj.getJSONObject("stats"))
        if (obj.optString("status") == "ok") {
            GatherTopicResult(
                success = true,
                title = obj.optString("title", topic),
                category = obj.optString("category", "General"),
                answer = obj.optString("answer", ""),
                sourceLabel = obj.optString("source_label", "Web"),
                stats = stats,
            )
        } else {
            GatherTopicResult(
                success = false,
                error = obj.optString("error", "Could not fetch topic online."),
                stats = stats,
            )
        }
    }

    suspend fun gatherStudyPack(packName: String): GatherPackResult = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("gather_study_pack", packName).toString()
        val obj = JSONObject(jsonStr)
        val stats = parseStats(obj.getJSONObject("stats"))
        if (obj.optString("status") == "ok") {
            GatherPackResult(
                success = true,
                savedCount = obj.optInt("saved", 0),
                totalCount = obj.optInt("total", 0),
                stats = stats,
            )
        } else {
            GatherPackResult(
                success = false,
                error = obj.optString("error", "Unable to download study pack."),
                stats = stats,
            )
        }
    }

    suspend fun getStudyPacks(): List<String> = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val arr = JSONArray(bridge.callAttr("get_study_packs").toString())
        List(arr.length()) { idx -> arr.getString(idx) }
    }

    suspend fun teach(
        question: String,
        answer: String,
        category: String,
        tags: String,
        replaceId: Int? = null,
    ): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr(
            "teach",
            question,
            answer,
            category,
            tags,
            replaceId ?: -1,
        ).toString()
        val obj = JSONObject(jsonStr)
        parseStats(obj.getJSONObject("stats"))
    }

    suspend fun reinforceAnswer(entryId: Int): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("reinforce_answer", entryId).toString()
        val obj = JSONObject(jsonStr)
        parseStats(obj.getJSONObject("stats"))
    }

    suspend fun getKnowledgeEntries(
        search: String = "",
        category: String = "All",
    ): List<KnowledgeEntry> = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("get_knowledge_entries", search, category).toString()
        val arr = JSONArray(jsonStr)
        val list = ArrayList<KnowledgeEntry>(arr.length())
        for (i in 0 until arr.length()) {
            val item = arr.getJSONObject(i)
            list.add(
                KnowledgeEntry(
                    id = item.getInt("id"),
                    question = item.getString("question"),
                    answer = item.getString("answer"),
                    category = item.optString("category", "General"),
                    tags = item.optString("tags", ""),
                    reinforcementWeight = item.optDouble("reinforcement_weight", 1.0),
                    timesUsed = item.optInt("times_used", 0),
                    source = item.optString("source", "seed"),
                    createdAt = item.optString("created_at", ""),
                    updatedAt = item.optString("updated_at", ""),
                )
            )
        }
        list
    }

    suspend fun searchVault(
        query: String = "",
        domain: String = "All",
        limit: Int = 30,
    ): List<VaultRecord> = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("search_vault", query, domain, limit).toString()
        val arr = JSONArray(jsonStr)
        val list = ArrayList<VaultRecord>(arr.length())
        for (i in 0 until arr.length()) {
            val item = arr.getJSONObject(i)
            list.add(
                VaultRecord(
                    id = item.getInt("id"),
                    domain = item.optString("domain", "General"),
                    topicKey = item.optString("topic_key", ""),
                    title = item.optString("title", ""),
                    fact = item.optString("fact", ""),
                )
            )
        }
        list
    }

    suspend fun updateKnowledgeEntry(
        entryId: Int,
        question: String,
        answer: String,
        category: String,
    ): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr(
            "update_knowledge_entry",
            entryId,
            question,
            answer,
            category,
        ).toString()
        val obj = JSONObject(jsonStr)
        parseStats(obj.getJSONObject("stats"))
    }

    suspend fun deleteKnowledgeEntry(entryId: Int): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("delete_knowledge_entry", entryId).toString()
        val obj = JSONObject(jsonStr)
        parseStats(obj.getJSONObject("stats"))
    }

    suspend fun getStats(): KnowledgeStats = withContext(Dispatchers.IO) {
        val bridge = getBridgeModule()
        val jsonStr = bridge.callAttr("get_stats").toString()
        parseStats(JSONObject(jsonStr))
    }

    private fun parseVaultStatus(obj: JSONObject?): VaultStatus {
        if (obj == null) return VaultStatus()
        val domMap = LinkedHashMap<String, Int>()
        val domObj = obj.optJSONObject("domain_counts")
        if (domObj != null) {
            val keys = domObj.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                domMap[k] = domObj.optInt(k, 0)
            }
        }
        return VaultStatus(
            totalRecords = obj.optInt("total_records", 0),
            targetRecords = obj.optInt("target_records", 1_050_000),
            isComplete = obj.optBoolean("is_complete", false),
            isHydrating = obj.optBoolean("is_hydrating", false),
            progress = obj.optDouble("progress", 0.0).toFloat(),
            stage = obj.optString("stage", "Ready"),
            sizeMb = obj.optDouble("size_mb", 0.0),
            domainCounts = domMap,
        )
    }

    private fun parseStats(obj: JSONObject): KnowledgeStats {
        val catMap = LinkedHashMap<String, Int>()
        val catObj = obj.optJSONObject("categories")
        if (catObj != null) {
            val keys = catObj.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                catMap[k] = catObj.optInt(k, 0)
            }
        }
        return KnowledgeStats(
            totalEntries = obj.optInt("total_entries", 0),
            seededCount = obj.optInt("seeded_count", 0),
            learnedCount = obj.optInt("learned_count", 0),
            onlineCachedCount = obj.optInt("online_cached_count", 0),
            vocabSize = obj.optInt("vocab_size", 0),
            totalInteractions = obj.optInt("total_interactions", 0),
            totalCorrections = obj.optInt("total_corrections", 0),
            avgReinforcement = obj.optDouble("avg_reinforcement", 1.0),
            categories = catMap,
            vault = parseVaultStatus(obj.optJSONObject("vault")),
        )
    }
}
