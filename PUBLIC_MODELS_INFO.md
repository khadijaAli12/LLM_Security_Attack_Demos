# Public Models (No Login Required) - Updated Info

## ✅ Truly Public Models (No Login)

These models can be tested **without any login**:

1. **QWEN** (Alibaba)
   - URL: HuggingFace Space
   - No login required
   - Direct access

2. **Llama** (Meta)
   - URL: HuggingFace Space  
   - No login required
   - Direct access

## ⚠️ Models Requiring Login

These models **require login** before testing:

1. **ChatGPT** (OpenAI)
   - Requires: OpenAI account login
   - Website: chat.openai.com

2. **Gemini** (Google)
   - Requires: Google account login
   - Website: gemini.google.com

3. **DeepSeek** 
   - Requires: Email/Google login
   - Website: chat.deepseek.com
   - **Note**: Previously thought to be public, but now requires login

## 🎯 Recommended Testing Approach

### For Quick Testing (No Login):
```bash
python run_security_tests.py
# When asked for models, type: qwen,llama
# Or type: public (default)
```

### For Complete Testing:
1. First test public models (QWEN, Llama)
2. Then manually login to ChatGPT/Gemini/DeepSeek
3. Run tests again with login-required models

## 📝 Updated Default Behavior

- **Default selection**: Only QWEN and Llama (truly public)
- **"Select Public Only" button**: Selects only QWEN and Llama
- **Login-required models**: Clearly marked with ⚠️ warning

## 🔄 Why DeepSeek Changed?

DeepSeek recently updated their website to require login for security and usage tracking. It's no longer accessible without authentication.


