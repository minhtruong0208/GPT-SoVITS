# vietnamese.py

import re
from typing import List, Tuple, Dict

# Vietnamese phoneme symbols
# Initials (phụ âm đầu)
INITIALS = [
    'b', 't', 'th', 'đ', 'ch', 'kh', 'g', 'h', 'l', 'm', 'n', 
    'nh', 'ph', 'r', 's', 'tr', 'v', 'x', 'qu', 'gi', 'k', 'ng', 'ngh',
    'c', 'd', 'p'  # Thêm các phụ âm đầu còn thiếu
]

# Finals (vần) - Đầy đủ các vần tiếng Việt
FINALS = [
    'a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y',
    'ai', 'ao', 'au', 'ay', 'eo', 'êu', 'ia', 'iê', 'iu', 'oa', 'oă', 
    'oe', 'oi', 'ôi', 'ơi', 'ua', 'uâ', 'ue', 'uê', 'ui', 'uo', 'ươ', 
    'uy', 'yê', 'ya', 'âu', 'ău', 'iêu', 'yêu', 'uôi', 'ươi', 'ươu',
    'an', 'ăn', 'ân', 'en', 'ên', 'in', 'on', 'ôn', 'ơn', 'un', 'ưn', 'yn',
    'ang', 'ăng', 'âng', 'eng', 'êng', 'ing', 'ong', 'ông', 'ơng', 'ung', 'ưng',
    'anh', 'ênh', 'inh', 'oanh', 'uênh',
    'ach', 'êch', 'ich', 'och', 'ôch', 'ơch', 'uch', 'ưch',
    'ac', 'ăc', 'âc', 'ec', 'êc', 'ic', 'oc', 'ôc', 'ơc', 'uc', 'ưc',
    'ap', 'ăp', 'âp', 'ep', 'êp', 'ip', 'op', 'ôp', 'ơp', 'up', 'ưp',
    'at', 'ăt', 'ât', 'et', 'êt', 'it', 'ot', 'ôt', 'ơt', 'ut', 'ưt'
]

# Tones (thanh điệu)
TONES = ['1', '2', '3', '4', '5', '6']  # Ngang, Huyền, Sắc, Hỏi, Ngã, Nặng

# Special tokens
SPECIAL = ['SP', 'SP2', 'SP3', 'UNK']

# All Vietnamese phoneme symbols
vietnamese_symbols = INITIALS + FINALS + TONES + SPECIAL

# Mapping dictionary for tone marks
TONE_MAPPING = {
    'à': ('a', '2'), 'á': ('a', '3'), 'ả': ('a', '4'), 'ã': ('a', '5'), 'ạ': ('a', '6'),
    'ằ': ('ă', '2'), 'ắ': ('ă', '3'), 'ẳ': ('ă', '4'), 'ẵ': ('ă', '5'), 'ặ': ('ă', '6'),
    'ầ': ('â', '2'), 'ấ': ('â', '3'), 'ẩ': ('â', '4'), 'ẫ': ('â', '5'), 'ậ': ('â', '6'),
    'è': ('e', '2'), 'é': ('e', '3'), 'ẻ': ('e', '4'), 'ẽ': ('e', '5'), 'ẹ': ('e', '6'),
    'ề': ('ê', '2'), 'ế': ('ê', '3'), 'ể': ('ê', '4'), 'ễ': ('ê', '5'), 'ệ': ('ê', '6'),
    'ì': ('i', '2'), 'í': ('i', '3'), 'ỉ': ('i', '4'), 'ĩ': ('i', '5'), 'ị': ('i', '6'),
    'ò': ('o', '2'), 'ó': ('o', '3'), 'ỏ': ('o', '4'), 'õ': ('o', '5'), 'ọ': ('o', '6'),
    'ồ': ('ô', '2'), 'ố': ('ô', '3'), 'ổ': ('ô', '4'), 'ỗ': ('ô', '5'), 'ộ': ('ô', '6'),
    'ờ': ('ơ', '2'), 'ớ': ('ơ', '3'), 'ở': ('ơ', '4'), 'ỡ': ('ơ', '5'), 'ợ': ('ơ', '6'),
    'ù': ('u', '2'), 'ú': ('u', '3'), 'ủ': ('u', '4'), 'ũ': ('u', '5'), 'ụ': ('u', '6'),
    'ừ': ('ư', '2'), 'ứ': ('ư', '3'), 'ử': ('ư', '4'), 'ữ': ('ư', '5'), 'ự': ('ư', '6'),
    'ỳ': ('y', '2'), 'ý': ('y', '3'), 'ỷ': ('y', '4'), 'ỹ': ('y', '5'), 'ỵ': ('y', '6')
}

def text_normalize(text: str) -> str:
    """
    Normalize Vietnamese text by removing extra spaces, converting to lowercase,
    and handling punctuation.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Normalized text
    """
    # Remove multiple spaces and trim
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace specific punctuation with comma
    text = re.sub(r'[;:"\']+', ',', text)
    
    # Keep only allowed punctuation
    text = re.sub(r'[^\w\s,.!?àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵđ]', '', text)
    
    return text

def find_tone(word: str) -> Tuple[str, str]:
    """
    Extract tone from a Vietnamese syllable and return the word without tone marks.
    
    Args:
        word (str): Input word with tone
        
    Returns:
        Tuple[str, str]: (word without tone, tone number)
    """
    tone = '1'  # Default tone (ngang)
    result = ''
    
    for char in word:
        if char in TONE_MAPPING:
            base, tone = TONE_MAPPING[char]
            result += base
        else:
            result += char
            
    return result, tone

def split_vietnamese_word(word: str) -> Tuple[str, str, str]:
    """
    Split a Vietnamese word into initial consonant, final part and tone.
    
    Args:
        word (str): Input word
        
    Returns:
        Tuple[str, str, str]: (initial, final, tone)
    """
    # First, extract tone and get clean word
    word_without_tone, tone = find_tone(word)
    
    # Find initial consonant
    initial = ''
    # Sort initials by length (longest first) to avoid partial matches
    sorted_initials = sorted(INITIALS, key=len, reverse=True)
    
    for i in sorted_initials:
        if word_without_tone.startswith(i):
            initial = i
            word_without_tone = word_without_tone[len(i):]
            break
    
    # The rest is final
    final = word_without_tone
    
    # Validate final
    if final not in FINALS:
        closest_final = find_closest_final(final)
        if closest_final:
            final = closest_final
    
    return initial, final, tone

def find_closest_final(final: str) -> str:
    """
    Find the closest matching final in case of inexact matches.
    This helps handle cases where the input might have slight variations.
    
    Args:
        final (str): Input final to match
        
    Returns:
        str: Closest matching final or empty string if no close match found
    """
    if final in FINALS:
        return final
        
    # Try common transformations
    transformations = [
        lambda x: x.replace('uo', 'ưo'),
        lambda x: x.replace('ua', 'ưa'),
        lambda x: x.replace('oi', 'ơi'),
        lambda x: x.replace('ou', 'ơu')
    ]
    
    for transform in transformations:
        transformed = transform(final)
        if transformed in FINALS:
            return transformed
            
    return final  # Return original if no transformation works

def g2p(text: str) -> Tuple[List[str], List[int]]:
    """
    Convert Vietnamese text to phonemes (Grapheme-to-Phoneme conversion).
    
    Args:
        text (str): Input text
        
    Returns:
        Tuple[List[str], List[int]]: (phonemes list, word to phoneme mapping)
    """
    normalized_text = text_normalize(text)
    words = normalized_text.split()
    phonemes = []
    word2ph = []
    
    for word in words:
        # Handle punctuation
        if word in [',', '.', '!', '?']:
            phonemes.append(word)
            word2ph.append(1)
            continue
        
        # Handle special tokens
        if word in SPECIAL:
            phonemes.append(word)
            word2ph.append(1)
            continue
            
        # Process Vietnamese word
        initial, final, tone = split_vietnamese_word(word)
        
        # Build phoneme sequence
        current_phonemes = []
        if initial:
            if initial not in INITIALS:
                initial = 'UNK'
            current_phonemes.append(initial)
            
        if final:
            if final not in FINALS:
                final = 'UNK'
            current_phonemes.append(final)
            
        if tone != '1':  # Only add non-neutral tones
            current_phonemes.append(tone)
            
        phonemes.extend(current_phonemes)
        word2ph.append(len(current_phonemes))
    
    return phonemes, word2ph

def test_vietnamese_g2p():
    """
    Test function for Vietnamese G2P conversion
    """
    test_cases = [
        "xin chào",
        "tôi yêu việt nam",
        "học sinh, giáo viên",
        "chương trình phát triển",
        "đường đi khó khăn",
        "tiếng việt thật đẹp!"
    ]
    
    print("Testing Vietnamese G2P conversion:")
    print("-" * 50)
    
    for text in test_cases:
        print(f"\nInput text: {text}")
        
        normalized = text_normalize(text)
        print(f"Normalized: {normalized}")
        
        phonemes, word2ph = g2p(normalized)
        print(f"Phonemes: {phonemes}")
        print(f"Word2ph: {word2ph}")
        
        # Validate output
        total_phonemes = sum(word2ph)
        assert len(phonemes) == total_phonemes, f"Phoneme count mismatch: {len(phonemes)} != {total_phonemes}"
        print("✓ Validation passed")

if __name__ == "__main__":
    test_vietnamese_g2p()
