package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoAwesomeMosaic
import androidx.compose.material.icons.rounded.ChatBubble
import androidx.compose.material.icons.rounded.MenuBook
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.ui.AiViewModel
import com.example.ui.components.GatherOnlineBottomSheet
import com.example.ui.components.TeachBottomSheet
import com.example.ui.screens.ChatScreen
import com.example.ui.screens.DashboardScreen
import com.example.ui.screens.KnowledgeInspectorScreen
import com.example.ui.theme.MeklitAiTheme

const val ROUTE_DASHBOARD = "dashboard"
const val ROUTE_CHAT = "chat"
const val ROUTE_INSPECTOR = "inspector"

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MeklitAiTheme {
                MayaApp()
            }
        }
    }
}

@Composable
fun MayaApp(
    viewModel: AiViewModel = viewModel(),
) {
    val navController = rememberNavController()
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route ?: ROUTE_DASHBOARD

    fun navigateTab(route: String) {
        if (route == ROUTE_INSPECTOR) {
            viewModel.updateInspectorFilter()
        }
        navController.navigate(route) {
            popUpTo(navController.graph.findStartDestination().id) {
                saveState = true
            }
            launchSingleTop = true
            restoreState = true
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface,
            ) {
                NavigationBarItem(
                    selected = currentRoute == ROUTE_DASHBOARD,
                    onClick = { navigateTab(ROUTE_DASHBOARD) },
                    icon = { Icon(Icons.Rounded.AutoAwesomeMosaic, contentDescription = null) },
                    label = { Text("Dashboard") },
                    modifier = Modifier.testTag("nav_tab_dashboard"),
                )
                NavigationBarItem(
                    selected = currentRoute == ROUTE_CHAT,
                    onClick = { navigateTab(ROUTE_CHAT) },
                    icon = { Icon(Icons.Rounded.ChatBubble, contentDescription = null) },
                    label = { Text("Maya Chat") },
                    modifier = Modifier.testTag("nav_tab_chat"),
                )
                NavigationBarItem(
                    selected = currentRoute == ROUTE_INSPECTOR,
                    onClick = { navigateTab(ROUTE_INSPECTOR) },
                    icon = { Icon(Icons.Rounded.MenuBook, contentDescription = null) },
                    label = { Text("Brain & 1M+") },
                    modifier = Modifier.testTag("nav_tab_inspector"),
                )
            }
        },
    ) { outerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = outerPadding.calculateBottomPadding()),
        ) {
            NavHost(
                navController = navController,
                startDestination = ROUTE_DASHBOARD,
            ) {
                composable(ROUTE_DASHBOARD) {
                    Box(modifier = Modifier.windowInsetsPadding(WindowInsets.statusBars)) {
                        DashboardScreen(
                            uiState = uiState,
                            onOpenChat = { navigateTab(ROUTE_CHAT) },
                            onRunQueryInChat = { query ->
                                navigateTab(ROUTE_CHAT)
                                viewModel.submitQuery(query)
                            },
                            onPrefillSummarizer = {
                                viewModel.onInputChanged("summarize: ")
                                navigateTab(ROUTE_CHAT)
                            },
                            onOpenTeach = {
                                viewModel.openTeachSheet(
                                    question = "",
                                    answer = "",
                                    category = "Learned",
                                    tags = "",
                                )
                            },
                            onOpenGather = { viewModel.openGatherSheet() },
                            onOpenVault = {
                                viewModel.setInspectorTab(1)
                                navigateTab(ROUTE_INSPECTOR)
                            },
                        )
                    }
                }

                composable(ROUTE_CHAT) {
                    ChatScreen(
                        uiState = uiState,
                        quickPrompts = viewModel.quickPrompts,
                        onInputChanged = viewModel::onInputChanged,
                        onSend = { viewModel.submitQuery() },
                        onSelectDomain = viewModel::onQuickDomainSelected,
                        onQuickPromptClick = { prompt -> viewModel.submitQuery(prompt.query) },
                        onHelpfulClick = viewModel::reinforceMessage,
                        onTeachClick = { q, a, cat, replaceId, msgId ->
                            viewModel.openTeachSheet(
                                question = q,
                                answer = a,
                                category = cat,
                                editingEntryId = replaceId,
                                targetMessageId = msgId,
                            )
                        },
                        onGatherOnlineTopic = viewModel::gatherTopicIntoChat,
                        onOpenGatherSheet = { viewModel.openGatherSheet() },
                        onOpenInspector = {
                            viewModel.setInspectorTab(0)
                            navigateTab(ROUTE_INSPECTOR)
                        },
                        onClearChat = viewModel::clearChat,
                        onDismissBanner = viewModel::dismissBanner,
                    )
                }

                composable(ROUTE_INSPECTOR) {
                    KnowledgeInspectorScreen(
                        uiState = uiState,
                        onBack = { navigateTab(ROUTE_DASHBOARD) },
                        onOpenGather = { viewModel.openGatherSheet() },
                        onTabChange = viewModel::setInspectorTab,
                        onSearchChange = { q -> viewModel.updateInspectorFilter(search = q) },
                        onCategoryChange = { cat -> viewModel.updateInspectorFilter(category = cat) },
                        onVaultSearchChange = { q -> viewModel.updateVaultFilter(search = q) },
                        onVaultDomainChange = { d -> viewModel.updateVaultFilter(domain = d) },
                        onAddNew = {
                            viewModel.openTeachSheet(
                                question = "",
                                answer = "",
                                category = "Learned",
                                tags = "",
                                editingEntryId = null,
                                targetMessageId = null,
                            )
                        },
                        onEditEntry = { entry ->
                            viewModel.openTeachSheet(
                                question = entry.question,
                                answer = entry.answer,
                                category = entry.category,
                                tags = entry.tags,
                                editingEntryId = entry.id,
                                targetMessageId = null,
                            )
                        },
                        onDeleteEntry = viewModel::deleteKnowledgeEntry,
                    )
                }
            }
        }
    }

    TeachBottomSheet(
        state = uiState.teachDialog,
        onDismiss = viewModel::closeTeachSheet,
        onSave = viewModel::saveTaughtKnowledge,
    )

    GatherOnlineBottomSheet(
        state = uiState.gatherSheet,
        isOnline = uiState.isOnline,
        autoGatherWhenOnline = uiState.autoGatherWhenOnline,
        onToggleAutoGather = viewModel::toggleAutoGather,
        onTopicChanged = viewModel::onGatherTopicChanged,
        onFetchTopic = viewModel::fetchTopicFromSheet,
        onFetchPack = viewModel::fetchStudyPackFromSheet,
        onDismiss = viewModel::closeGatherSheet,
    )
}
