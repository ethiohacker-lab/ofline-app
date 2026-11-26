package com.example.ui.components

import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import com.example.ui.theme.MonoFontFamily

@Composable
fun FormattedResponseText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyLarge,
) {
    val codeBg = MaterialTheme.colorScheme.surfaceVariant
    val codeFg = MaterialTheme.colorScheme.primary

    val annotated = remember(text, codeBg, codeFg) {
        parseSimpleFormatting(text, codeBg, codeFg)
    }

    Text(
        text = annotated,
        style = style,
        color = MaterialTheme.colorScheme.onSurface,
        modifier = modifier,
    )
}

private fun parseSimpleFormatting(
    input: String,
    codeBg: androidx.compose.ui.graphics.Color,
    codeFg: androidx.compose.ui.graphics.Color,
): AnnotatedString {
    return buildAnnotatedString {
        var i = 0
        while (i < input.length) {
            if (i + 1 < input.length && input[i] == '*' && input[i + 1] == '*') {
                val end = input.indexOf("**", startIndex = i + 2)
                if (end != -1) {
                    withStyle(SpanStyle(fontWeight = FontWeight.Bold)) {
                        append(input.substring(i + 2, end))
                    }
                    i = end + 2
                    continue
                }
            }
            if (input[i] == '`') {
                val end = input.indexOf('`', startIndex = i + 1)
                if (end != -1) {
                    withStyle(
                        SpanStyle(
                            fontFamily = MonoFontFamily,
                            background = codeBg,
                            color = codeFg,
                            fontWeight = FontWeight.Medium,
                        )
                    ) {
                        append(" ${input.substring(i + 1, end)} ")
                    }
                    i = end + 1
                    continue
                }
            }
            append(input[i])
            i++
        }
    }
}
