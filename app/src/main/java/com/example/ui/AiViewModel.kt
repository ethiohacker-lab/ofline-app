package com.example.ui

import android.app.Application
import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.PythonAiRepository
import com.example.model.AiResponse
import com.example.model.ChatMessage
import com.example.model.GatherOnlineState
import com.example.model.KnowledgeEntry
import com.example.model.KnowledgeStats
import com.example.model.QuickDomain
import com.example.model.QuickPrompt
import com.example.model.TeachDialogState
import com.example.model.VaultRecord
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class AiUiState(
    val isInitializing: Boolean = true,
    val isThinking: Boolean = false,
    val isOnline: Boolean = false,
    val autoGatherWhenOnline: Boolean = true,
    val initError: String? = null,
    val inputQuery: String = "",
    val selectedQuickDomain: QuickDomain = QuickDomain.ALL,
    val messages: List<ChatMessage> = emptyList(),
    val stats: KnowledgeStats = KnowledgeStats(),
    val teachDialog: TeachDialogState = TeachDialogState(),
    val gatherSheet: GatherOnlineState = GatherOnlineState(),
    val inspectorEntries: List<KnowledgeEntry> = emptyList(),
    val inspectorSearch: String = "",
    val inspectorCategory: String = "All",
    val inspectorTab: Int = 0, // 0 = Semantic Brain, 1 = 1M+ Vault
    val vaultSearch: String = "",
    val vaultDomain: String = "All",
    val vaultResults: List<VaultRecord> = emptyList(),
    val statusBanner: String? = null,
)

class AiViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = PythonAiRepository(application)
    private val connectivityManager =
        application.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

    private val _uiState = MutableStateFlow(AiUiState(isOnline = checkIsOnline()))
    val uiState: StateFlow<AiUiState> = _uiState.asStateFlow()

    val quickPrompts: List<QuickPrompt> = listOf(
        // English & Offline Power Tools
        QuickPrompt(QuickDomain.ENGLISH, "Say Hello", "Good morning Maya, how are you?"),
        QuickPrompt(QuickDomain.ENGLISH, "Define Word", "define resilience"),
        QuickPrompt(QuickDomain.ENGLISH, "Offline Summarizer", "summarize: Arabica coffee grows best in Ethiopian highlands between 1500 and 2100 meters altitude. Shade trees regulate leaf temperature and prevent overbearing dieback. Wet processing yields bright floral acidity while dry natural processing gives sweet heavy body."),
        QuickPrompt(QuickDomain.ENGLISH, "Study Quiz", "quiz me"),
        QuickPrompt(QuickDomain.ENGLISH, "Ethiopic Unicode", "unicode 4608"),
        // Math
        QuickPrompt(QuickDomain.MATH, "Number 1729 Vault", "number 1729"),
        QuickPrompt(QuickDomain.MATH, "Quadratic Solver", "solve 2x^2 - 5x + 2 = 0"),
        QuickPrompt(QuickDomain.MATH, "Matrix Inverse", "matrix [[2,1],[5,3]]"),
        QuickPrompt(QuickDomain.MATH, "RCBD Stats", "stats 42.5, 44.1, 39.8, 45.0, 41.2"),
        QuickPrompt(QuickDomain.MATH, "Hectare to Timad", "2.5 ha to timad"),
        // Horticulture
        QuickPrompt(QuickDomain.HORTICULTURE, "Urea Dosage", "fertilizer urea 100 kg/ha 2 timad"),
        QuickPrompt(QuickDomain.HORTICULTURE, "Plant Spacing", "spacing 0.75 x 0.30 area 1 ha"),
        QuickPrompt(QuickDomain.HORTICULTURE, "Spray Dilution", "dilution c1 50 c2 0.5 v2 20"),
        QuickPrompt(QuickDomain.HORTICULTURE, "Arabica Coffee", "What are optimal growing conditions for Arabica coffee?"),
        QuickPrompt(QuickDomain.HORTICULTURE, "Enset & Kocho", "Explain Enset false banana propagation and kocho"),
        // Computer Science
        QuickPrompt(QuickDomain.CS, "Port 443 Vault", "port 443"),
        QuickPrompt(QuickDomain.CS, "IPv4 Subnet", "subnet 192.168.10.0/26"),
        QuickPrompt(QuickDomain.CS, "Base Convert", "convert 255 to binary"),
        QuickPrompt(QuickDomain.CS, "Big-O QuickSort", "big o quicksort"),
        QuickPrompt(QuickDomain.CS, "3NF Normalization", "Explain database normalization 1NF 2NF and 3NF"),
    )

    private val networkCallback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            _uiState.update { it.copy(isOnline = true) }
        }

        override fun onLost(network: Network) {
            _uiState.update { it.copy(isOnline = checkIsOnline()) }
        }

        override fun onCapabilitiesChanged(network: Network, networkCapabilities: NetworkCapabilities) {
            val validated = networkCapabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            _uiState.update { it.copy(isOnline = validated) }
        }
    }

    init {
        registerNetworkObserver()
        initializeBrain()
    }

    private fun checkIsOnline(): Boolean {
        val active = connectivityManager.activeNetwork ?: return false
        val caps = connectivityManager.getNetworkCapabilities(active) ?: return false
        return caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    private fun registerNetworkObserver() {
        try {
            val request = NetworkRequest.Builder()
                .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()
            connectivityManager.registerNetworkCallback(request, networkCallback)
        } catch (_: Exception) {
        }
    }

    override fun onCleared() {
        super.onCleared()
        try {
            connectivityManager.unregisterNetworkCallback(networkCallback)
        } catch (_: Exception) {
        }
    }

    private fun initializeBrain() {
        viewModelScope.launch {
            try {
                val stats = repository.initialize()
                val entries = repository.getKnowledgeEntries()
                val packs = repository.getStudyPacks()
                val vaultSample = if (stats.vault.isComplete) {
                    repository.searchVault("", "All", 25)
                } else {
                    emptyList()
                }
                _uiState.update {
                    it.copy(
                        isInitializing = false,
                        initError = null,
                        stats = stats,
                        inspectorEntries = entries,
                        vaultResults = vaultSample,
                        gatherSheet = it.gatherSheet.copy(studyPacks = packs),
                    )
                }
                if (!stats.vault.isComplete) {
                    monitorVaultHydration()
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isInitializing = false,
                        initError = e.localizedMessage ?: "Failed to start Maya's embedded Python engine.",
                    )
                }
            }
        }
    }

    private fun monitorVaultHydration() {
        viewModelScope.launch {
            var checks = 0
            while (checks < 180) {
                delay(650)
                checks++
                val stats = try {
                    repository.getStats()
                } catch (_: Exception) {
                    continue
                }
                _uiState.update { it.copy(stats = stats) }
                if (stats.vault.isComplete) {
                    val sample = repository.searchVault(
                        _uiState.value.vaultSearch,
                        _uiState.value.vaultDomain,
                        25,
                    )
                    _uiState.update { it.copy(vaultResults = sample) }
                    break
                }
                if (!stats.vault.isHydrating && checks > 5) {
                    break
                }
            }
        }
    }

    fun onInputChanged(text: String) {
        _uiState.update { it.copy(inputQuery = text) }
    }

    fun onQuickDomainSelected(domain: QuickDomain) {
        _uiState.update { it.copy(selectedQuickDomain = domain) }
    }

    fun toggleAutoGather(enabled: Boolean) {
        _uiState.update {
            it.copy(
                autoGatherWhenOnline = enabled,
                statusBanner = if (enabled) {
                    "Auto-Gather enabled: when online, Maya saves web answers for offline use."
                } else {
                    "Strict Offline mode: Maya answers only from local SQLite & math engine."
                },
            )
        }
    }

    fun submitQuery(explicitQuery: String? = null) {
        val raw = (explicitQuery ?: _uiState.value.inputQuery).trim()
        if (raw.isEmpty() || _uiState.value.isThinking || _uiState.value.isInitializing) return

        val stateSnapshot = _uiState.value
        val allowOnline = stateSnapshot.isOnline && stateSnapshot.autoGatherWhenOnline

        val userMsg = ChatMessage(isUser = true, text = raw)
        _uiState.update {
            it.copy(
                inputQuery = if (explicitQuery == null) "" else it.inputQuery,
                isThinking = true,
                messages = it.messages + userMsg,
                statusBanner = null,
            )
        }

        viewModelScope.launch {
            try {
                val response = repository.ask(raw, allowOnlineFetch = allowOnline)
                val updatedStats = repository.getStats()
                val refreshedEntries = if (response.route == "online_cached") {
                    repository.getKnowledgeEntries(
                        _uiState.value.inspectorSearch,
                        _uiState.value.inspectorCategory,
                    )
                } else {
                    _uiState.value.inspectorEntries
                }
                val aiMsg = ChatMessage(
                    isUser = false,
                    text = response.answer,
                    userQueryForMessage = raw,
                    aiResponse = response,
                )
                _uiState.update {
                    it.copy(
                        isThinking = false,
                        messages = it.messages + aiMsg,
                        stats = updatedStats,
                        inspectorEntries = refreshedEntries,
                    )
                }
            } catch (e: Exception) {
                val errMsg = ChatMessage(
                    isUser = false,
                    text = "Offline engine error: ${e.localizedMessage ?: "Unknown Python error"}",
                    userQueryForMessage = raw,
                )
                _uiState.update {
                    it.copy(
                        isThinking = false,
                        messages = it.messages + errMsg,
                    )
                }
            }
        }
    }

    fun gatherTopicIntoChat(topic: String) {
        if (_uiState.value.isThinking) return
        _uiState.update { it.copy(isThinking = true) }
        viewModelScope.launch {
            val res = repository.gatherTopicOnline(topic)
            val refreshed = repository.getKnowledgeEntries(
                _uiState.value.inspectorSearch,
                _uiState.value.inspectorCategory,
            )
            val msg = if (res.success) {
                ChatMessage(
                    isUser = false,
                    text = res.answer,
                    userQueryForMessage = topic,
                    aiResponse = AiResponse(
                        answer = res.answer,
                        confidence = 0.94,
                        route = "online_cached",
                        category = res.category,
                        matchedId = null,
                        matchedQuestion = res.title,
                        needsTeaching = false,
                        closestGuess = null,
                        formulaSteps = "Saved to SQLite from ${res.sourceLabel} — now available 100% offline",
                        tag = "Cached (${res.sourceLabel})",
                    ),
                )
            } else {
                ChatMessage(
                    isUser = false,
                    text = res.error ?: "Could not fetch topic online. Check your internet connection or teach Maya manually.",
                    userQueryForMessage = topic,
                )
            }
            _uiState.update {
                it.copy(
                    isThinking = false,
                    stats = res.stats,
                    inspectorEntries = refreshed,
                    messages = it.messages + msg,
                )
            }
        }
    }

    fun openGatherSheet(initialTopic: String = "") {
        _uiState.update {
            it.copy(
                gatherSheet = it.gatherSheet.copy(
                    isOpen = true,
                    topicInput = initialTopic,
                    resultMessage = null,
                )
            )
        }
    }

    fun closeGatherSheet() {
        _uiState.update {
            it.copy(gatherSheet = it.gatherSheet.copy(isOpen = false, isFetching = false))
        }
    }

    fun onGatherTopicChanged(text: String) {
        _uiState.update {
            it.copy(gatherSheet = it.gatherSheet.copy(topicInput = text))
        }
    }

    fun fetchTopicFromSheet() {
        val topic = _uiState.value.gatherSheet.topicInput.trim()
        if (topic.isEmpty() || _uiState.value.gatherSheet.isFetching) return
        _uiState.update {
            it.copy(gatherSheet = it.gatherSheet.copy(isFetching = true, resultMessage = null))
        }
        viewModelScope.launch {
            val res = repository.gatherTopicOnline(topic)
            val entries = repository.getKnowledgeEntries(
                _uiState.value.inspectorSearch,
                _uiState.value.inspectorCategory,
            )
            _uiState.update {
                it.copy(
                    stats = res.stats,
                    inspectorEntries = entries,
                    gatherSheet = it.gatherSheet.copy(
                        isFetching = false,
                        topicInput = if (res.success) "" else it.gatherSheet.topicInput,
                        resultMessage = if (res.success) {
                            "Saved \"${res.title}\" (${res.category}) from ${res.sourceLabel} to offline SQLite!"
                        } else {
                            res.error ?: "Failed to fetch online."
                        },
                    ),
                )
            }
        }
    }

    fun fetchStudyPackFromSheet(packName: String) {
        if (_uiState.value.gatherSheet.isFetching) return
        _uiState.update {
            it.copy(gatherSheet = it.gatherSheet.copy(isFetching = true, resultMessage = "Downloading $packName…"))
        }
        viewModelScope.launch {
            val res = repository.gatherStudyPack(packName)
            val entries = repository.getKnowledgeEntries(
                _uiState.value.inspectorSearch,
                _uiState.value.inspectorCategory,
            )
            _uiState.update {
                it.copy(
                    stats = res.stats,
                    inspectorEntries = entries,
                    gatherSheet = it.gatherSheet.copy(
                        isFetching = false,
                        resultMessage = if (res.success) {
                            "Cached ${res.savedCount}/${res.totalCount} topics from $packName into SQLite for offline study!"
                        } else {
                            res.error ?: "Failed to download pack."
                        },
                    ),
                )
            }
        }
    }

    fun reinforceMessage(messageId: String, entryId: Int) {
        viewModelScope.launch {
            try {
                val updatedStats = repository.reinforceAnswer(entryId)
                val refreshed = repository.getKnowledgeEntries(
                    _uiState.value.inspectorSearch,
                    _uiState.value.inspectorCategory,
                )
                _uiState.update { state ->
                    state.copy(
                        stats = updatedStats,
                        inspectorEntries = refreshed,
                        messages = state.messages.map { msg ->
                            if (msg.id == messageId) msg.copy(isReinforced = true) else msg
                        },
                        statusBanner = "Reinforced! Maya boosted this entry's weight in SQLite.",
                    )
                }
            } catch (_: Exception) {
            }
        }
    }

    fun openTeachSheet(
        question: String = "",
        answer: String = "",
        category: String = "Learned",
        tags: String = "",
        editingEntryId: Int? = null,
        targetMessageId: String? = null,
    ) {
        _uiState.update {
            it.copy(
                teachDialog = TeachDialogState(
                    isOpen = true,
                    editingEntryId = editingEntryId,
                    initialQuestion = question,
                    initialAnswer = answer,
                    initialCategory = category,
                    initialTags = tags,
                    targetMessageId = targetMessageId,
                )
            )
        }
    }

    fun closeTeachSheet() {
        _uiState.update { it.copy(teachDialog = TeachDialogState(isOpen = false)) }
    }

    fun saveTaughtKnowledge(
        question: String,
        answer: String,
        category: String,
        tags: String,
    ) {
        val q = question.trim()
        val a = answer.trim()
        if (q.isEmpty() || a.isEmpty()) return

        val dialogState = _uiState.value.teachDialog
        viewModelScope.launch {
            try {
                val stats = if (dialogState.editingEntryId != null && dialogState.targetMessageId == null) {
                    repository.updateKnowledgeEntry(
                        entryId = dialogState.editingEntryId,
                        question = q,
                        answer = a,
                        category = category,
                    )
                } else {
                    repository.teach(
                        question = q,
                        answer = a,
                        category = category,
                        tags = tags,
                        replaceId = dialogState.editingEntryId,
                    )
                }
                val entries = repository.getKnowledgeEntries(
                    _uiState.value.inspectorSearch,
                    _uiState.value.inspectorCategory,
                )

                val learnConfirm = if (dialogState.targetMessageId != null) {
                    listOf(
                        ChatMessage(
                            isUser = false,
                            text = "Learned & indexed! Next time you ask about \"$q\", Maya will recall your verified answer from SQLite.",
                            userQueryForMessage = q,
                        )
                    )
                } else {
                    emptyList()
                }

                _uiState.update { state ->
                    state.copy(
                        stats = stats,
                        inspectorEntries = entries,
                        teachDialog = TeachDialogState(isOpen = false),
                        messages = state.messages + learnConfirm,
                        statusBanner = "Saved to SQLite & rebuilt Maya's NumPy matrix (${stats.vocabSize} terms).",
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        teachDialog = TeachDialogState(isOpen = false),
                        statusBanner = "Save failed: ${e.localizedMessage}",
                    )
                }
            }
        }
    }

    fun setInspectorTab(tabIndex: Int) {
        _uiState.update { it.copy(inspectorTab = tabIndex) }
        if (tabIndex == 1 && _uiState.value.vaultResults.isEmpty()) {
            updateVaultFilter()
        }
    }

    fun updateInspectorFilter(search: String? = null, category: String? = null) {
        val nextSearch = search ?: _uiState.value.inspectorSearch
        val nextCat = category ?: _uiState.value.inspectorCategory
        _uiState.update {
            it.copy(inspectorSearch = nextSearch, inspectorCategory = nextCat)
        }
        viewModelScope.launch {
            val entries = repository.getKnowledgeEntries(nextSearch, nextCat)
            _uiState.update { it.copy(inspectorEntries = entries) }
        }
    }

    fun updateVaultFilter(search: String? = null, domain: String? = null) {
        val nextSearch = search ?: _uiState.value.vaultSearch
        val nextDom = domain ?: _uiState.value.vaultDomain
        _uiState.update {
            it.copy(vaultSearch = nextSearch, vaultDomain = nextDom)
        }
        viewModelScope.launch {
            val rows = repository.searchVault(nextSearch, nextDom, 30)
            _uiState.update { it.copy(vaultResults = rows) }
        }
    }

    fun deleteKnowledgeEntry(entryId: Int) {
        viewModelScope.launch {
            val stats = repository.deleteKnowledgeEntry(entryId)
            val entries = repository.getKnowledgeEntries(
                _uiState.value.inspectorSearch,
                _uiState.value.inspectorCategory,
            )
            _uiState.update {
                it.copy(
                    stats = stats,
                    inspectorEntries = entries,
                    statusBanner = "Entry removed and Maya's index updated.",
                )
            }
        }
    }

    fun clearChat() {
        _uiState.update { it.copy(messages = emptyList(), statusBanner = null) }
    }

    fun dismissBanner() {
        _uiState.update { it.copy(statusBanner = null) }
    }
}
