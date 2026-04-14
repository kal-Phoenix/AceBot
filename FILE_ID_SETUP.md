# 📁 File ID Setup Guide

Simple guide to set up AceBot with file_id-based content delivery.

## 🎯 Overview

AceBot uses **direct file_id mapping** for content delivery:
- **Simple file_id configuration**
- **Direct file delivery to users**
- **Private channel storage**
- **No external dependencies**

## 🔧 Setup Process

### 1. Upload Files to Your Private Channel

1. Create a private Telegram channel (only you and your bot)
2. Add your bot as admin with post permissions
3. Upload your educational files to the channel

### 2. Extract File IDs

Use the included extractor bot:

1. **Start extractor:** `python extractor.py`
2. **Forward files** from your channel to `@file_id12bot`
3. **Copy file_ids** from the responses

**Example Response:**
```
📄 DOCUMENT

File: Grade_9_Math.pdf
FILE_ID: BAADBAADAwADBREAAR4BAAFPVkVOVGVyAg

Configuration:
{"file_id": "BAADBAADAwADBREAAR4BAAFPVkVOVGVyAg", "name": "Grade_9_Math.pdf", "type": "document"}
```

### 3. Configure File Mapping

Edit `services/telegram_channel.py` and update the `_get_file_ids_mapping()` function:

```python
def _get_file_ids_mapping(self, content_key: str) -> List[Dict]:
    file_mapping = {
        # Free Textbooks
        "natural_textbook_grade9": [
            {
                "file_id": "BAADBAADAwADBREAAR4BAAFPVkVOVGVyAg",  # Your actual file_id
                "name": "Grade 9 Mathematics Textbook", 
                "type": "document"
            },
            {
                "file_id": "BAADBAADBAADBREAAR4BAAFPVkVOVGVyAg",  # Your actual file_id
                "name": "Grade 9 Physics Textbook", 
                "type": "document"
            },
        ],
        
        # Premium Notes
        "natural_notes_math": [
            {
                "file_id": "BAADBAADCQADBREAAr4BAAFPVkVOVGVyAg",  # Your actual file_id
                "name": "Mathematics Short Notes - Algebra", 
                "type": "document"
            },
        ],
        
        # Add more mappings for your content...
    }
    
    return file_mapping.get(content_key, [])
```

## 📋 Content Key Structure

The system automatically builds content keys based on user requests:

### Free Content
- `natural_textbook_grade9` → Natural stream, Grade 9 textbooks
- `social_guide_grade10` → Social stream, Grade 10 teacher's guides
- `natural_pastexam_2010` → Natural stream, 2010 past exam (free)

### Premium Content  
- `natural_notes_math` → Natural stream, Mathematics notes
- `natural_cheats_physics` → Natural stream, Physics cheat sheets
- `natural_quiz_math_grade9` → Natural stream, Math quiz for Grade 9
- `natural_quiz_math_mixed` → Natural stream, Math quiz mixed grades
- `natural_pastexam_2015` → Natural stream, 2015 past exam (premium)
- `natural_examtips` → Natural stream, exam tips
- `social_studytips` → Social stream, study tips

## 🔄 Content Categories

### **Free Resources**
```python
# Textbooks
"natural_textbook_grade9": [...],
"natural_textbook_grade10": [...],
"social_textbook_grade9": [...],

# Teacher's Guides  
"natural_guide_grade9": [...],
"social_guide_grade10": [...],

# Past Exams (2000-2013)
"natural_pastexam_2010": [...],
"social_pastexam_2012": [...],
```

### **Premium Resources**
```python
# Short Notes
"natural_notes_math": [...],
"natural_notes_physics": [...],
"social_notes_geography": [...],

# Cheat Sheets
"natural_cheats_math": [...],
"natural_cheats_chemistry": [...],
"social_cheats_history": [...],

# Quizzes
"natural_quiz_math_grade9": [...],
"natural_quiz_physics_mixed": [...],
"social_quiz_economics_grade11": [...],

# Past Exams (2014-2017)
"natural_pastexam_2015": [...],
"social_pastexam_2016": [...],

# Tips
"natural_examtips": [...],
"social_studytips": [...],
```

## 🚀 How It Works

### User Request Flow
1. **User**: "📚 Resources → 📖 Text Books → Grade 9 Textbooks"
2. **Bot**: Builds key `natural_textbook_grade9`
3. **Service**: Looks up file_ids for that key
4. **Bot**: Sends files directly to user using file_ids
5. **User**: Receives actual files in their chat

### Example
```
Content Key: "natural_textbook_grade9"
↓
File IDs: ["BAADBAADAwADBREAAR4BAAFPVkVOVGVyAg", "BAADBAADBAADBREAAR4BAAFPVkVOVGVyAg"]
↓
Bot sends files directly to user
↓
User receives: "Grade 9 Mathematics Textbook.pdf", "Grade 9 Physics Textbook.pdf"
```

## ✅ Benefits of File ID Approach

1. **Simplicity** - No hashtag parsing or channel message searching
2. **Reliability** - Direct file access using Telegram's file system
3. **Performance** - Faster than message forwarding
4. **Maintenance** - Easy to add/remove files by updating mapping
5. **Security** - Files stored in your private channel, delivered securely
6. **Flexibility** - Easy to organize files by any categorization system

## 🛠️ Adding New Content

### Step-by-Step Process

1. **Upload File** to your private channel
2. **Get File ID** using @userinfobot  
3. **Update Mapping** in `services/telegram_channel.py`
4. **Test** through the bot

### Example: Adding a New Math Quiz

1. Upload `Math_Quiz_Grade10.pdf` to your channel
2. Forward to @userinfobot → Get file_id: `BAADBAADNewFileId123`
3. Add to mapping:
```python
"natural_quiz_math_grade10": [
    {
        "file_id": "BAADBAADNewFileId123",
        "name": "Math Quiz - Grade 10 Advanced",
        "type": "document"
    },
],
```
4. Test: User requests Grade 10 Math Quiz → Bot sends the file

## 🔧 Configuration Tips

### File Types
- **Documents**: PDFs, Word docs, etc. → `"type": "document"`
- **Images**: JPGs, PNGs, etc. → `"type": "photo"`
- Most educational content will be `"document"`

### File Names
- Use descriptive names that users will understand
- Include grade/subject information when helpful
- Keep names concise but informative

### Organization
- Group related files under the same content key
- Use consistent naming conventions
- Consider creating separate keys for different difficulty levels

This approach provides the simplest and most reliable content delivery system while maintaining all the security and premium control features of your bot!
