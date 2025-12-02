export async function predictText(text) {
   // e.g. if text contains 'bad' → 'negative', else 'positive'
    // return { prediction, confidence }
    if (text.toLowerCase().includes('bad')) {
        return { prediction: 'negative', confidence: 0.9 };
    } else {
        return { prediction: 'positive', confidence: 0.9 };
    }
}