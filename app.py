import streamlit as st
import os
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Nusaybah Hub - Your Trusted Shopping Hub",
    page_icon="🏢",
    layout="centered"
)

# ------------------------------------------------------------------
# BRAND COLORS (Update these hex codes to match your exact brand)
# ------------------------------------------------------------------
BRAND_PRIMARY = "#0B1A3A"   # Deep Navy Blue (Matches your trusted hub vibe)
BRAND_ACCENT = "#D4AF37"    # Gold (Premium feel)
BRAND_WHITE = "#FFFFFF"
BRAND_LIGHT_BG = "#F8F9FA"

# ------------------------------------------------------------------
# BUSINESS INFORMATION (Updated from your image)
# ------------------------------------------------------------------
business_info = {
    "name": "NUSAYBAH HUB",
    "tagline": "YOUR TRUSTED SHOPPING HUB",
    "address": "C/73 Alhaji Ango Street, Jos North, Plateau State, Nigeria",
    "phone": "08105257672",
    "whatsapp": "08105257672",
    "hours": {
        "Monday-Thursday": "8:00 AM – 6:00 PM",
        "Friday": "8:00 AM – 5:00 PM",
        "Saturday-Sunday": "8:00 AM – 6:00 PM"
    },
    "offerings": {
        "fashion": "Modest fashion, thrift abayas (₦7,000), thick hand sleeves (₦800), fashion pins, and visor hats.",
        "electronics": "Quality electronics and gadgets.",
        "tailoring": "Custom garment construction and fashion design (Nusaybah Power and Stitch).",
        "home_appliances": "Home appliances and household gadgets.",
        "thrift": "Affordable luxury thrift items."
    },
    "shipping": "Reliable local delivery across Jos and nationwide shipping throughout Nigeria.",
    "social_media": {
        "facebook": "https://www.facebook.com/100077686659565/",
        "instagram": "https://www.instagram.com/nusaybahyaaqub/"
    }
}

# Initialize OpenAI client (use OPENAI_API_KEY from Streamlit secrets)
api_key = st.secrets.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key) if api_key else None

# ------------------------------------------------------------------
# PROFESSIONAL BRANDED CSS
# ------------------------------------------------------------------
st.markdown(f"""
    <style>
    /* Main container styling */
    .main {{
        background-color: {BRAND_LIGHT_BG};
    }}
    
    /* Brand Header */
    .brand-header {{
        background: {BRAND_PRIMARY};
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 4px solid {BRAND_ACCENT};
    }}
    .brand-name {{
        color: {BRAND_WHITE};
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1.2;
    }}
    .brand-tagline {{
        color: {BRAND_ACCENT};
        font-size: 1.1rem;
        font-weight: 500;
        letter-spacing: 5px;
        margin-top: 0.2rem;
    }}
    .brand-categories {{
        color: {BRAND_WHITE};
        font-size: 0.9rem;
        font-weight: 300;
        letter-spacing: 2px;
        margin-top: 0.8rem;
        opacity: 0.9;
    }}
    .brand-phone {{
        color: {BRAND_WHITE};
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 0.5rem;
        background: {BRAND_ACCENT};
        color: {BRAND_PRIMARY};
        display: inline-block;
        padding: 0.2rem 1.5rem;
        border-radius: 20px;
    }}
    
    /* Quick buttons styling */
    .stButton > button {{
        background-color: {BRAND_PRIMARY};
        color: {BRAND_WHITE};
        border: 1px solid {BRAND_PRIMARY};
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stButton > button:hover {{
        background-color: {BRAND_ACCENT};
        color: {BRAND_PRIMARY};
        border-color: {BRAND_ACCENT};
        transform: scale(1.02);
    }}
    
    /* Response box */
    .response-box {{
        background-color: {BRAND_WHITE};
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid {BRAND_ACCENT};
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        color: {BRAND_PRIMARY};
        font-size: 1rem;
        line-height: 1.6;
    }}
    .response-box strong {{
        color: {BRAND_PRIMARY};
    }}
    
    /* Footer */
    .brand-footer {{
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 2px solid #E0E0E0;
        text-align: center;
        color: #6B7280;
        font-size: 0.85rem;
    }}
    .brand-footer strong {{
        color: {BRAND_PRIMARY};
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# BRAND HEADER (Matches your image exactly)
# ------------------------------------------------------------------
st.markdown(f"""
    <div class="brand-header">
        <div class="brand-name">NUSAYBAH HUB</div>
        <div class="brand-tagline">YOUR TRUSTED SHOPPING HUB</div>
        <div class="brand-categories">
            FASHION • ELECTRONICS • TAILORING • HOME APPLIANCES • THRIFT
        </div>
        <div class="brand-phone">📞 {business_info['phone']}</div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# QUICK ACTION BUTTONS
# ------------------------------------------------------------------
st.subheader("Quick Questions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📍 Address"):
        st.session_state.query = "What is your address?"
with col2:
    if st.button("📞 Contact"):
        st.session_state.query = "How can I contact you?"
with col3:
    if st.button("🕐 Hours"):
        st.session_state.query = "What are your business hours?"
with col4:
    if st.button("📦 Shipping"):
        st.session_state.query = "Do you ship nationwide?"

# ------------------------------------------------------------------
# SEARCH BAR
# ------------------------------------------------------------------
user_query = st.text_input(
    "Ask me anything about Nusaybah Hub:",
    value=st.session_state.get("query", ""),
    placeholder="e.g., Do you have electronics? or What thrift items do you sell?"
)

# ------------------------------------------------------------------
# Q&A ENGINE
# ------------------------------------------------------------------
def get_static_response(query):
    """Check if query matches known patterns"""
    q = query.lower()
    
    # Address
    if any(word in q for word in ["address", "location", "where", "store", "shop"]):
        return f"📍 **Our Address:**\n\n{business_info['address']}\n\nYou can get directions on Google Maps."
    
    # Phone/Contact
    if any(word in q for word in ["phone", "contact", "call", "whatsapp", "reach", "number"]):
        return f"📞 **Contact Us:**\n\nPhone / WhatsApp: {business_info['phone']}\n\nWe respond to messages within 24 hours."
    
    # Hours
    if any(word in q for word in ["hour", "time", "open", "close", "when"]):
        hours_text = "\n".join([f"- {day}: {time}" for day, time in business_info["hours"].items()])
        return f"🕐 **Business Hours:**\n\n{hours_text}\n\nWe are closed on public holidays."
    
    # Fashion / Abaya / Sleeves / Pins / Visor
    if any(word in q for word in ["fashion", "abaya", "₦7000", "7000", "thrift", "sleeve", "hand", "₦800", "800", "pin", "visor", "hat"]):
        return f"👗 **Fashion & Accessories:**\n\n{business_info['offerings']['fashion']}\n\nVisit our store or contact us via WhatsApp to see current stock."
    
    # Electronics
    if any(word in q for word in ["electronics", "gadget", "tech", "device"]):
        return f"📱 **Electronics:**\n\n{business_info['offerings']['electronics']}\n\nWe offer quality electronics and gadgets. Contact us for current availability and prices."
    
    # Tailoring
    if any(word in q for word in ["tailor", "custom", "sew", "design", "stitch"]):
        return f"✂️ **Tailoring:**\n\n{business_info['offerings']['tailoring']}\n\nWe specialize in modest fashion designs. Contact us to discuss your specific needs."
    
    # Home Appliances
    if any(word in q for word in ["appliance", "home appliance", "household", "kitchen"]):
        return f"🏠 **Home Appliances:**\n\n{business_info['offerings']['home_appliances']}\n\nWe offer a range of home appliances. Contact us to inquire about our current stock and prices."
    
    # General offerings / What do you sell?
    if any(word in q for word in ["offer", "sell", "product", "service", "what do you do", "categories"]):
        offerings_text = "\n".join([f"- **{category.replace('_', ' ').title()}**: {description}" for category, description in business_info["offerings"].items()])
        return f"🛍️ **What We Offer:**\n\n{offerings_text}\n\nContact us for more details or to place an order!"
    
    # Shipping
    if any(word in q for word in ["ship", "delivery", "shipping", "nationwide", "deliver"]):
        return f"📦 **Shipping & Delivery:**\n\n{business_info['shipping']}\n\nLocal delivery within Jos City is available. Nationwide shipping across Nigeria is also offered."
    
    # Social Media
    if any(word in q for word in ["facebook", "instagram", "social", "follow"]):
        return f"📱 **Follow Us:**\n\nFacebook: {business_info['social_media']['facebook']}\n\nInstagram: {business_info['social_media']['instagram']}"
    
    return None

# Process query
if user_query:
    with st.spinner("Thinking..."):
        static_response = get_static_response(user_query)
        
        if static_response:
            st.markdown(f'<div class="response-box">{static_response}</div>', unsafe_allow_html=True)
        else:
            if client is not None:
                try:
                    system_prompt = f"""You are the AI assistant for Nusaybah Hub, a trusted shopping hub in Jos, Nigeria. 
                    
Here is our business information:
- Name: NUSAYBAH HUB
- Tagline: YOUR TRUSTED SHOPPING HUB
- Address: {business_info['address']}
- Phone/WhatsApp: {business_info['phone']}
- Business Hours: {business_info['hours']}
- Offerings: {business_info['offerings']}
- Shipping: {business_info['shipping']}
- Facebook: {business_info['social_media']['facebook']}
- Instagram: {business_info['social_media']['instagram']}

Answer questions helpfully, concisely, and professionally. If you don't know something, say so and offer to connect the user with our team at {business_info['phone']}."""
                    
                    completion = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_query}
                        ],
                        temperature=0.3,
                        max_tokens=500
                    )
                    response = completion.choices[0].message.content
                    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"I couldn't process your question. Please try again or contact us directly at {business_info['phone']}")
            else:
                st.info(f"❓ I don't have a specific answer for that question.\n\n**Contact us directly:**\n\n📞 Phone/WhatsApp: {business_info['phone']}\n📍 Address: {business_info['address']}")

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown(f"""
    <div class="brand-footer">
        <strong>NUSAYBAH HUB</strong> — Your Trusted Shopping Hub<br>
        FASHION • ELECTRONICS • TAILORING • HOME APPLIANCES • THRIFT<br>
        📍 {business_info['address']} &nbsp;|&nbsp; 📞 {business_info['phone']}
    </div>
""", unsafe_allow_html=True)
