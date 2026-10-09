import streamlit as st
import google.generativeai as genai

# Streamlit Secrets से API Key पढ़ना
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# प्रोजेक्ट का डेटा
PROJECT_KNOWLEDGE = """
प्रोजेक्ट शीर्षक: पारंपरिक और डिजिटल शिक्षा का संगम (Traditional vs Digital Learning)

आधार 1: Digital + Traditional Learning (मिश्रित शिक्षण)
- पारंपरिक ब्लैकबोर्ड/किताबों और डिजिटल एनिमेशन/स्क्रीन का संतुलन।
- थ्योरी किताबों से और विज़ुअलाइज़ेशन डिजिटल माध्यम से।

आधार 2: T.L.M (Teaching Learning Material - शिक्षण अधिगम सामग्री)
- हस्तनिर्मित चार्ट, 3D मॉडल, फ्लैशकार्ड और मूर्त सामग्री।
- बच्चे चीज़ों को छूकर और देखकर सीखते हैं।

आधार 3: Low Cost Smart Class (किफायती स्मार्ट क्लासरूम)
- महंगे स्मार्ट बोर्ड की जगह कम कीमत वाले प्रोजेक्टर, टीवी स्क्रीन या स्मार्टफोन का उपयोग।
- कम बजट वाले ग्रामीण और सरकारी स्कूलों के लिए प्रभावी समाधान।

आधार 4: Inclusive Education (समावेशी शिक्षा)
- दिव्यांग और विशेष आवश्यकता वाले बच्चों को सामान्य बच्चों के साथ पढ़ाना।
- ऑडियो टूल्स, ब्रेल सामग्री, स्क्रीन रीडर और रैंप जैसी सुविधाएं।

आधार 5: Activity Based Learning (गतिविधि आधारित शिक्षा)
- रटने की जगह 'करके सीखना' (Learning by Doing)।
- रोल-प्ले, पहेलियाँ, विज्ञान प्रयोग और गणितीय खेल।

आधार 6: Eco-Friendly School (पर्यावरण अनुकूल विद्यालय)
- प्लास्टिक-मुक्त परिसर, वेस्ट मटेरियल से टी.एल.एम. बनाना।
- वर्षा जल संचयन (Rainwater harvesting) और पेपरलेस काम।
"""

system_prompt = f"""
तुम 'शिक्षा सेतु AI' हो।
तुम्हारा काम स्कूल प्रोजेक्ट "पारंपरिक और डिजिटल शिक्षा" के 6 आधारों को समझाना है:
{PROJECT_KNOWLEDGE}

नियम:
1. हमेशा सरल, आदरपूर्ण और स्पष्ट हिंदी में उत्तर दो।
2. उत्तर छोटे और 2-3 मुख्य बिंदुओं में दो ताकि पढ़ने में आसानी हो।
3. केवल शिक्षा और इन 6 आधारों से जुड़े सवालों के जवाब दो।
"""

# AI मॉडल सेटअप
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# वेब पेज लेआउट
st.set_page_config(page_title="शिक्षा सेतु AI Assistant", page_icon="🏫", layout="wide")

# साइडबार
with st.sidebar:
    st.header("📌 6 मुख्य आधार")
    st.markdown("""
    1. **Digital + Traditional Learning**
    2. **T.L.M (Teaching Material)**
    3. **Low Cost Smart Class**
    4. **Inclusive Education**
    5. **Activity Based Learning**
    6. **Eco-Friendly School**
    """)
    st.divider()
    st.info("किसी भी आधार पर सवाल पूछने के लिए चैट बॉक्स का उपयोग करें।")

st.title("🎓 पारंपरिक एवं डिजिटल शिक्षा AI गाइड")
st.caption("हमारे स्कूल मॉडल के 6 स्तंभों के बारे में जानकारी प्राप्त करें।")

# चैट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "नमस्ते! मैं 'शिक्षा सेतु AI' हूँ। आप हमारे स्कूल प्रोजेक्ट के 6 आधारों में से किसी पर भी सवाल पूछ सकते हैं।"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("अपना सवाल यहाँ लिखें (उदा. Low Cost Smart Class कैसे काम करती है?)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("सोच रहा हूँ..."):
        response = model.generate_content(user_input)
        bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)
