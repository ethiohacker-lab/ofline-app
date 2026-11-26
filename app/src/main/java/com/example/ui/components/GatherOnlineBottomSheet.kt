package com.example.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.CloudDownload
import androidx.compose.material.icons.rounded.CloudOff
import androidx.compose.material.icons.rounded.DownloadDone
import androidx.compose.material.icons.rounded.LibraryAdd
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.example.R
import com.example.model.GatherOnlineState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GatherOnlineBottomSheet(
    state: GatherOnlineState,
    isOnline: Boolean,
    autoGatherWhenOnline: Boolean,
    onToggleAutoGather: (Boolean) -> Unit,
    onTopicChanged: (String) -> Unit,
    onFetchTopic: () -> Unit,
    onFetchPack: (String) -> Unit,
    onDismiss: () -> Unit,
) {
    if (!state.isOpen) return

    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = MaterialTheme.colorScheme.surface,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
                .padding(bottom = 24.dp)
                .navigationBarsPadding()
                .imePadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Icon(
                    imageVector = if (isOnline) Icons.Rounded.CloudDownload else Icons.Rounded.CloudOff,
                    contentDescription = null,
                    tint = if (isOnline) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                )
                Column {
                    Text(
                        text = stringResource(R.string.gather_sheet_title),
                        style = MaterialTheme.typography.titleLarge,
                    )
                    Text(
                        text = if (isOnline) "Connected • Ready to cache into SQLite" else "Currently Offline • Cached items still work offline",
                        style = MaterialTheme.typography.labelMedium,
                        color = if (isOnline) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                    )
                }
            }

            Text(
                text = stringResource(R.string.gather_sheet_subtitle),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Surface(
                shape = RoundedCornerShape(14.dp),
                color = MaterialTheme.colorScheme.surfaceVariant,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Column(modifier = Modifier.weight(1f).padding(end = 10.dp)) {
                        Text(
                            text = "Auto-Gather Unknown Topics",
                            style = MaterialTheme.typography.labelLarge,
                        )
                        Text(
                            text = "When online, automatically fetch & store unknown questions for offline use.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Switch(
                        checked = autoGatherWhenOnline,
                        onCheckedChange = onToggleAutoGather,
                        modifier = Modifier.testTag("auto_gather_switch"),
                    )
                }
            }

            OutlinedTextField(
                value = state.topicInput,
                onValueChange = onTopicChanged,
                label = { Text(stringResource(R.string.gather_topic_label)) },
                placeholder = { Text("e.g., Photosynthesis or define eloquent") },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("gather_topic_input"),
            )

            Button(
                onClick = onFetchTopic,
                enabled = isOnline && state.topicInput.isNotBlank() && !state.isFetching,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp)
                    .testTag("gather_fetch_button"),
            ) {
                if (state.isFetching) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = MaterialTheme.colorScheme.onPrimary,
                    )
                    Spacer(Modifier.width(8.dp))
                } else {
                    Icon(Icons.Rounded.CloudDownload, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                }
                Text(stringResource(R.string.gather_fetch_btn))
            }

            if (state.studyPacks.isNotEmpty()) {
                Text(
                    text = "One-Tap Offline Study Packs (5 Topics Each)",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(top = 4.dp),
                )
                state.studyPacks.forEach { pack ->
                    OutlinedButton(
                        onClick = { onFetchPack(pack) },
                        enabled = isOnline && !state.isFetching,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.5f)),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp)
                            .testTag("gather_pack_${pack.lowercase().replace(" ", "_")}"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.LibraryAdd,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                        )
                        Spacer(Modifier.width(8.dp))
                        Text("Download $pack")
                    }
                }
            }

            state.resultMessage?.let { msg ->
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.primaryContainer,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.DownloadDone,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onPrimaryContainer,
                        )
                        Text(
                            text = msg,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                        )
                    }
                }
            }
        }
    }
}
