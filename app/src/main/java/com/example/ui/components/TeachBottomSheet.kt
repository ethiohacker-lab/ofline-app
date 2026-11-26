package com.example.ui.components

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoFixHigh
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Psychology
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.example.R
import com.example.model.TeachDialogState

private val TEACH_CATEGORIES = listOf("English", "Horticulture", "Computer Science", "Math", "General", "Learned")

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TeachBottomSheet(
    state: TeachDialogState,
    onDismiss: () -> Unit,
    onSave: (question: String, answer: String, category: String, tags: String) -> Unit,
) {
    if (!state.isOpen) return

    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var question by remember(state) { mutableStateOf(state.initialQuestion) }
    var answer by remember(state) { mutableStateOf(state.initialAnswer) }
    var category by remember(state) {
        mutableStateOf(
            if (state.initialCategory in TEACH_CATEGORIES) state.initialCategory else "Learned"
        )
    }
    var tags by remember(state) { mutableStateOf(state.initialTags) }

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
                    imageVector = if (state.editingEntryId != null) Icons.Rounded.AutoFixHigh else Icons.Rounded.Psychology,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                )
                Text(
                    text = stringResource(
                        if (state.editingEntryId != null) R.string.teach_sheet_title_edit
                        else R.string.teach_sheet_title_new
                    ),
                    style = MaterialTheme.typography.titleLarge,
                )
            }

            Text(
                text = stringResource(R.string.teach_sheet_subtitle),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            OutlinedTextField(
                value = question,
                onValueChange = { question = it },
                label = { Text(stringResource(R.string.teach_question_label)) },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("teach_question_input"),
                minLines = 2,
                maxLines = 4,
            )

            OutlinedTextField(
                value = answer,
                onValueChange = { answer = it },
                label = { Text(stringResource(R.string.teach_answer_label)) },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("teach_answer_input"),
                minLines = 3,
                maxLines = 7,
            )

            Text(
                text = stringResource(R.string.teach_category_label),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurface,
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                TEACH_CATEGORIES.forEach { cat ->
                    val selected = category == cat
                    FilterChip(
                        selected = selected,
                        onClick = { category = cat },
                        label = { Text(cat) },
                        leadingIcon = if (selected) {
                            { Icon(Icons.Rounded.Check, contentDescription = null) }
                        } else null,
                        modifier = Modifier.testTag("teach_category_${cat.lowercase().replace(" ", "_")}"),
                    )
                }
            }

            OutlinedTextField(
                value = tags,
                onValueChange = { tags = it },
                label = { Text(stringResource(R.string.teach_tags_label)) },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("teach_tags_input"),
                singleLine = true,
            )

            Spacer(modifier = Modifier.height(4.dp))

            Button(
                onClick = { onSave(question, answer, category, tags) },
                enabled = question.isNotBlank() && answer.isNotBlank(),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .testTag("teach_save_button"),
            ) {
                Text(stringResource(R.string.teach_save_btn))
            }
        }
    }
}
