package com.example.model

import java.util.UUID

data class ClosestGuess(
    val id: Int,
    val question: String,
    val answer: String,
    val category: String,
    val confidence: Double,
)

data class AiResponse(
    val answer: String,
    val confidence: Double,
    val route: String,
    val category: String,
    val matchedId: Int?,
    val matchedQuestion: String?,
    val needsTeaching: Boolean,
    val closestGuess: ClosestGuess?,
    val formulaSteps: String,
    val tag: String,
)

data class ChatMessage(
    val id: String = UUID.randomUUID().toString(),
    val isUser: Boolean,
    val text: String,
    val userQueryForMessage: String = "",
    val aiResponse: AiResponse? = null,
    val isReinforced: Boolean = false,
)

data class KnowledgeEntry(
    val id: Int,
    val question: String,
    val answer: String,
    val category: String,
    val tags: String,
    val reinforcementWeight: Double,
    val timesUsed: Int,
    val source: String,
    val createdAt: String,
    val updatedAt: String,
)

data class VaultStatus(
    val totalRecords: Int = 0,
    val targetRecords: Int = 1_050_000,
    val isComplete: Boolean = false,
    val isHydrating: Boolean = false,
    val progress: Float = 0f,
    val stage: String = "Preparing 1.05M+ Offline Vault…",
    val sizeMb: Double = 0.0,
    val domainCounts: Map<String, Int> = emptyMap(),
)

data class VaultRecord(
    val id: Int,
    val domain: String,
    val topicKey: String,
    val title: String,
    val fact: String,
)

data class KnowledgeStats(
    val totalEntries: Int = 0,
    val seededCount: Int = 0,
    val learnedCount: Int = 0,
    val onlineCachedCount: Int = 0,
    val vocabSize: Int = 0,
    val totalInteractions: Int = 0,
    val totalCorrections: Int = 0,
    val avgReinforcement: Double = 1.0,
    val categories: Map<String, Int> = emptyMap(),
    val vault: VaultStatus = VaultStatus(),
) {
    val combinedOfflineRecords: Int
        get() = totalEntries + vault.totalRecords
}

enum class QuickDomain(val label: String) {
    ALL("Featured"),
    ENGLISH("English"),
    MATH("Math"),
    HORTICULTURE("Horticulture"),
    CS("CS"),
}

data class QuickPrompt(
    val domain: QuickDomain,
    val title: String,
    val query: String,
)

data class TeachDialogState(
    val isOpen: Boolean = false,
    val editingEntryId: Int? = null,
    val initialQuestion: String = "",
    val initialAnswer: String = "",
    val initialCategory: String = "Learned",
    val initialTags: String = "",
    val targetMessageId: String? = null,
)

data class GatherOnlineState(
    val isOpen: Boolean = false,
    val isFetching: Boolean = false,
    val topicInput: String = "",
    val studyPacks: List<String> = emptyList(),
    val resultMessage: String? = null,
)
