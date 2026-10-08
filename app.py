from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io
import os

app = Flask(__name__)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD",)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "digigrow-dev-secret"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///digigrow.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    business = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    confidence = db.Column(db.Integer, nullable=False)
    online_presence = db.Column(db.Integer, nullable=False)
    challenges = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ModuleProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_slug = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(150), nullable=False)
    views = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


MODULES = {
    "social-media": {
    "title": "Social Media Marketing",
    "icon": "📱",
    "description": "Learn how to use Instagram step by step to create a professional business presence, attract customers and promote products or services.",
    
    "content": [
        {
            "heading": "Build your Instagram presence",
            "text": "Start from zero by creating an Instagram account and setting up a professional business profile."
        },
        {
            "heading": "Create business content",
            "text": "Learn how to create posts, Stories and Reels that showcase products, services and useful information."
        },
        {
            "heading": "Connect with customers",
            "text": "Learn how to respond to comments and messages and communicate professionally with potential customers."
        },
        {
            "heading": "Measure your progress",
            "text": "Use Instagram's Professional Dashboard and available insights to understand how your content is performing."
        }
    ],

    "topics": [
        "Instagram account setup",
        "Professional profile",
        "Instagram posts",
        "Instagram Stories",
        "Instagram Reels",
        "Customer engagement",
        "Professional Dashboard",
        "Instagram Insights"
    ],

    "tips": [
        "Use a simple username that customers can remember.",
        "Use a clear business logo or profile photo.",
        "Keep your business bio short and useful.",
        "Post clear and relevant photos or videos.",
        "Do not share your password or verification codes.",
        "Reply politely and professionally to customers.",
        "Avoid posting private customer information.",
        "Check your Professional Dashboard regularly."
    ],

    "lessons": [
        {
            "title": "Create and Set Up Your Instagram Account",
            "icon": "📱",
            "description": "Learn how to create an Instagram account and turn it into a professional business presence from the beginning.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare before you begin",
                    "text": "Keep your business name, logo or profile photo, phone number or email address, short business description and a suitable username idea ready."
                },
                {
                    "number": "1",
                    "title": "Create your Instagram account",
                    "text": "Open Instagram and choose the option to create a new account. Register using your email address or phone number and create a strong password."
                },
                {
                    "number": "2",
                    "title": "Choose a business-friendly username",
                    "text": "Choose a username that is simple, easy to remember and connected to your business name. Avoid unnecessary numbers or complicated characters when possible."
                },
                {
                    "number": "3",
                    "title": "Add your profile photo",
                    "text": "Upload your business logo or a clear image that represents your business. Make sure the image remains easy to recognize when displayed as a small profile picture."
                },
                {
                    "number": "4",
                    "title": "Write your Instagram bio",
                    "text": "Write a short description explaining what your business offers and who it serves. Keep the information clear and easy for a new visitor to understand."
                },
                {
                    "number": "5",
                    "title": "Add useful business information",
                    "text": "Add appropriate contact or business information so customers know how they can reach you."
                },
                {
                    "number": "6",
                    "title": "Switch to a Professional account",
                    "text": "Open your Instagram profile and find the account or professional-account settings. Follow the setup process to switch from a personal account to a Professional account."
                },
                {
                    "number": "7",
                    "title": "Choose the appropriate professional type",
                    "text": "If Instagram provides Business and Creator options, choose Business when it matches the purpose of your small business."
                },
                {
                    "number": "8",
                    "title": "Check your completed profile",
                    "text": "Review your username, profile photo, bio, category and contact information. Make sure a customer can understand your business quickly."
                }
            ],
            "activity": "Create a sample Instagram business profile and complete the username, profile photo, bio and professional-account setup.",
            "visual": "activities/social-media-account-guide.png"
        },

        {
            "title": "Create Your First Instagram Post",
            "icon": "📸",
            "description": "Learn how to create a simple promotional post for a product or service.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your content",
                    "text": "Choose a clear product or service photo. Prepare the product name, price if relevant, a short description and a way for customers to contact you."
                },
                {
                    "number": "1",
                    "title": "Open the Create option",
                    "text": "Open Instagram and use the create or add-post option from the Instagram interface."
                },
                {
                    "number": "2",
                    "title": "Select your photo",
                    "text": "Choose the product or service image you prepared. Select an image that is clear, well-lit and easy to understand."
                },
                {
                    "number": "3",
                    "title": "Check or edit the image",
                    "text": "Review the image and make simple adjustments if necessary. Avoid excessive editing that makes the product look different from reality."
                },
                {
                    "number": "4",
                    "title": "Write the caption",
                    "text": "Write the product or service name, its main benefit, important details and a simple call-to-action."
                },
                {
                    "number": "5",
                    "title": "Add relevant information",
                    "text": "Add relevant hashtags, location information or other useful details when appropriate. Only use information that genuinely relates to the post."
                },
                {
                    "number": "6",
                    "title": "Review the post",
                    "text": "Check the photo, caption, price, spelling, contact details and any other information before publishing."
                },
                {
                    "number": "7",
                    "title": "Publish the post",
                    "text": "Publish the post when everything is correct. If you are not ready, use the available draft option if appropriate."
                },
                {
                    "number": "8",
                    "title": "Check the published post",
                    "text": "Open the post after publishing and make sure the image, caption and business information appear correctly."
                }
            ],
            "activity": "Create one sample promotional Instagram post for a real or imaginary small business.",
            "visual": "activities/social-media-post-guide.png"
        },

        {
            "title": "Create an Instagram Story",
            "icon": "⭕",
            "description": "Learn how to use Instagram Stories to share temporary updates, offers and behind-the-scenes content.",
            "steps": [
                {
                    "number": "0",
                    "title": "Choose your Story idea",
                    "text": "Decide what you want to share, such as a new product, special offer, customer update, behind-the-scenes activity or useful tip."
                },
                {
                    "number": "1",
                    "title": "Open the Story creator",
                    "text": "Open Instagram and select the option to create a new Story."
                },
                {
                    "number": "2",
                    "title": "Select or create your content",
                    "text": "Choose a suitable photo or video from your device or create new content using the camera."
                },
                {
                    "number": "3",
                    "title": "Add useful information",
                    "text": "Add text, stickers or other suitable elements that help customers understand the message."
                },
                {
                    "number": "4",
                    "title": "Check your Story",
                    "text": "Review the Story and make sure the text is readable and the information is accurate."
                },
                {
                    "number": "5",
                    "title": "Publish your Story",
                    "text": "Publish the Story and check that it appears correctly on your profile."
                }
            ],
            "activity": "Create a sample Story announcing a new product, special offer or business update.",
            "visual": "activities/social-media-story-guide.png"
        },

        {
            "title": "Create an Instagram Reel",
            "icon": "🎬",
            "description": "Learn the basic process of creating a short video to showcase your business.",
            "steps": [
                {
                    "number": "0",
                    "title": "Plan your short video",
                    "text": "Choose one simple idea, such as showing a product, demonstrating a service, sharing a quick tip or showing how something is made."
                },
                {
                    "number": "1",
                    "title": "Open the Reel creator",
                    "text": "Open Instagram and select the option to create a Reel."
                },
                {
                    "number": "2",
                    "title": "Record or select a video",
                    "text": "Record a short video or select a suitable video from your device."
                },
                {
                    "number": "3",
                    "title": "Edit the video",
                    "text": "Trim the video and add suitable text or other available editing elements when useful."
                },
                {
                    "number": "4",
                    "title": "Add a clear message",
                    "text": "Make sure viewers can understand what your business is showing or offering."
                },
                {
                    "number": "5",
                    "title": "Write the caption",
                    "text": "Add a short caption that explains the Reel and encourages an appropriate customer action."
                },
                {
                    "number": "6",
                    "title": "Review and publish",
                    "text": "Check the video, text and caption before publishing the Reel."
                }
            ],
            "activity": "Create a short sample Reel showing a product, service, business tip or behind-the-scenes activity.",
            "visual": "activities/social-media-reel-guide.png"
        },

        {
            "title": "Engage With Customers",
            "icon": "💬",
            "description": "Learn how to communicate with customers through Instagram comments and messages.",
            "steps": [
                {
                    "number": "0",
                    "title": "Check your notifications",
                    "text": "Regularly check your Instagram notifications so you can notice new comments, messages and customer interactions."
                },
                {
                    "number": "1",
                    "title": "Read customer questions",
                    "text": "Read the customer's complete question before replying."
                },
                {
                    "number": "2",
                    "title": "Give a clear answer",
                    "text": "Provide accurate information about products, services, prices, availability or other relevant questions."
                },
                {
                    "number": "3",
                    "title": "Respond professionally",
                    "text": "Use polite and friendly language, even when a customer is unhappy or asks a repeated question."
                },
                {
                    "number": "4",
                    "title": "Move private information to private communication",
                    "text": "Do not publicly share customer phone numbers, addresses, payment information or other private details."
                },
                {
                    "number": "5",
                    "title": "Follow up when appropriate",
                    "text": "If a customer has shown genuine interest, provide the next useful information such as contact details, ordering instructions or business hours."
                }
            ],
            "activity": "Write three sample replies to common customer questions about a product or service.",
            "visual": "activities/social-media-engagement-guide.png"
        },

        {
            "title": "Use the Instagram Professional Dashboard",
            "icon": "📊",
            "description": "Learn how to use the Professional Dashboard and available insights to understand your Instagram activity and improve future content.",
            "steps": [
                {
                    "number": "0",
                    "title": "Make sure your account is professional",
                    "text": "The Professional Dashboard is associated with professional Instagram accounts. Make sure your account has been set up appropriately."
                },
                {
                    "number": "1",
                    "title": "Open your Instagram profile",
                    "text": "Open Instagram and go to your professional business profile."
                },
                {
                    "number": "2",
                    "title": "Open the Professional Dashboard",
                    "text": "Find and open the Professional Dashboard from your professional profile. Menu placement and labels may vary between app versions."
                },
                {
                    "number": "3",
                    "title": "Explore the available tools",
                    "text": "Look through the tools and resources provided for professional accounts and identify the sections that are useful for your business."
                },
                {
                    "number": "4",
                    "title": "Check account activity",
                    "text": "Review the available account activity information to understand how people are interacting with your content."
                },
                {
                    "number": "5",
                    "title": "Check content performance",
                    "text": "Look at the available information for your posts, Stories or Reels and identify which content receives useful engagement."
                },
                {
                    "number": "6",
                    "title": "Understand your audience information",
                    "text": "Review the audience information available to your professional account and use it to understand who is interacting with your content."
                },
                {
                    "number": "7",
                    "title": "Use the information to improve",
                    "text": "Use what you learn from your available insights to decide what type of content you should create more often."
                }
            ],
            "activity": "Open the Professional Dashboard and record three useful pieces of information about your account or content performance.",
            "visual": "activities/social-media-dashboard-guide.png"
        }
    ],

    "activity": "Complete the Social Media Marketing lessons in order. Create a professional Instagram profile, make a sample post, create a Story or Reel, practise responding to customers and explore the Professional Dashboard.",

    "steps": [
        {
            "number": "0",
            "title": "Start with the Instagram account setup lesson",
            "text": "Begin with the first topic and complete the account and professional-profile setup."
        },
        {
            "number": "1",
            "title": "Create your first business post",
            "text": "Move to the posting lesson and create a sample promotional post."
        },
        {
            "number": "2",
            "title": "Practise Stories and Reels",
            "text": "Create sample visual content to practise different Instagram formats."
        },
        {
            "number": "3",
            "title": "Practise customer engagement",
            "text": "Write sample replies to common customer questions and enquiries."
        },
        {
            "number": "4",
            "title": "Finish with the Professional Dashboard",
            "text": "Open the dashboard and learn how to use the available information to improve future content."
        }
    ],

    "visual": "activities/social-media-guide.png"
},

    "canva": {
    "title": "Canva for Small Business",
    "icon": "🎨",
    "description": "Learn how to use Canva from the beginning to create professional posters, social media graphics, promotional designs and business materials.",

    "content": [
        {
            "heading": "Start with Canva",
            "text": "Create or sign in to a Canva account and learn how to find the right design and template for your business."
        },
        {
            "heading": "Create business designs",
            "text": "Learn how to customise templates with your own business name, images, colours, text and contact information."
        },
        {
            "heading": "Create social media content",
            "text": "Learn how to create designs suitable for Instagram and other social media platforms."
        },
        {
            "heading": "Promote your business",
            "text": "Create promotional offers, announcements and other visual content that can help attract customers."
        }
    ],

    "topics": [
        "Creating a Canva account",
        "Understanding the Canva home screen",
        "Choosing design types",
        "Using templates",
        "Editing text",
        "Adding images",
        "Changing colours",
        "Adding logos",
        "Instagram designs",
        "Promotional posters",
        "Business branding",
        "Downloading designs"
    ],

    "tips": [
        "Keep your designs simple and easy to read.",
        "Use clear, high-quality images.",
        "Do not put too much text on one design.",
        "Use the same business colours and logo consistently.",
        "Make important information such as prices and contact details easy to notice.",
        "Check spelling before downloading or sharing a design.",
        "Choose the correct design size for the platform where you will use it."
    ],

    "lessons": [
        {
            "title": "Create and Set Up Your Canva Account",
            "icon": "🎨",
            "description": "Learn how to get started with Canva and understand the basic Canva workspace.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare before you begin",
                    "text": "Keep your business name, logo, product images and basic business information ready before starting your design."
                },
                {
                    "number": "1",
                    "title": "Open Canva",
                    "text": "Open Canva using the Canva website or app and choose the option to sign in or create an account."
                },
                {
                    "number": "2",
                    "title": "Create or sign in to your account",
                    "text": "Create a Canva account using an available sign-in method, or sign in if you already have an account."
                },
                {
                    "number": "3",
                    "title": "Explore the Canva home screen",
                    "text": "Look through the main Canva workspace and identify where you can create a design, search for templates and access your previous designs."
                },
                {
                    "number": "4",
                    "title": "Search for a design",
                    "text": "Use the search or design options to find the type of content you want to create, such as a poster or social media post."
                },
                {
                    "number": "5",
                    "title": "Choose a suitable template",
                    "text": "Select a template that matches your business purpose. Choose a design that is clear and easy to customise."
                },
                {
                    "number": "6",
                    "title": "Open the design editor",
                    "text": "Open the selected design and identify the main editing areas, such as text, images, elements and design controls."
                }
            ],
            "activity": "Create a Canva account or sign in and find one suitable template for a small business design.",
            "visual": "activities/canva-account-guide.png"
        },

        {
            "title": "Create Your First Business Poster",
            "icon": "🖼️",
            "description": "Learn how to turn a Canva template into a simple professional poster for a small business.",
            "steps": [
                {
                    "number": "0",
                    "title": "Choose your poster purpose",
                    "text": "Decide what the poster should communicate, such as a product announcement, service, new arrival or business information."
                },
                {
                    "number": "1",
                    "title": "Choose a poster template",
                    "text": "Search Canva for a poster design and choose a template that matches the type of business information you want to present."
                },
                {
                    "number": "2",
                    "title": "Change the business name",
                    "text": "Select the template text and replace it with your own business name."
                },
                {
                    "number": "3",
                    "title": "Add your product or service",
                    "text": "Replace the sample text with the name and important information about your product or service."
                },
                {
                    "number": "4",
                    "title": "Add your own image",
                    "text": "Upload or select a suitable product or business image and replace the sample image in the template."
                },
                {
                    "number": "5",
                    "title": "Edit colours and fonts",
                    "text": "Adjust colours and fonts so the design matches your business identity while keeping the text easy to read."
                },
                {
                    "number": "6",
                    "title": "Add contact information",
                    "text": "Add useful information such as a phone number, website, social media username or other appropriate contact method."
                },
                {
                    "number": "7",
                    "title": "Review the poster",
                    "text": "Check spelling, image quality, alignment, colours and contact information before downloading."
                },
                {
                    "number": "8",
                    "title": "Download the poster",
                    "text": "Use Canva's download option and select an appropriate file format for the way you plan to use the poster."
                }
            ],
            "activity": "Create a complete promotional poster for a real or imaginary small business.",
            "visual": "activities/canva-poster-guide.png"
        },

        {
            "title": "Create an Instagram Post",
            "icon": "📱",
            "description": "Learn how to create a social media graphic in Canva that can be used to promote a product or service.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your content",
                    "text": "Prepare a product photo, business name, product name, price if relevant and a short message for customers."
                },
                {
                    "number": "1",
                    "title": "Choose an Instagram design",
                    "text": "Search Canva for an Instagram post design or choose a suitable social media design size."
                },
                {
                    "number": "2",
                    "title": "Select a template",
                    "text": "Choose a clean template that provides enough space for your product image and important information."
                },
                {
                    "number": "3",
                    "title": "Add your product image",
                    "text": "Upload or select your product image and place it in the design."
                },
                {
                    "number": "4",
                    "title": "Edit the text",
                    "text": "Replace the template text with your product name, offer or other important business information."
                },
                {
                    "number": "5",
                    "title": "Add price or offer details",
                    "text": "If appropriate, add the product price, discount or other information customers need to know."
                },
                {
                    "number": "6",
                    "title": "Add your business identity",
                    "text": "Add your logo, business colours or other consistent branding elements."
                },
                {
                    "number": "7",
                    "title": "Check the design",
                    "text": "Make sure the text is readable, the image is clear and all important information is visible."
                },
                {
                    "number": "8",
                    "title": "Download the design",
                    "text": "Download the finished design in a suitable image format so it can be uploaded to Instagram or another platform."
                }
            ],
            "activity": "Create one Instagram-ready promotional graphic for a product or service.",
            "visual": "activities/canva-instagram-guide.png"
        },

        {
            "title": "Create a Promotional Offer",
            "icon": "📢",
            "description": "Learn how to create an attractive promotional design for a discount, special offer or business announcement.",
            "steps": [
                {
                    "number": "0",
                    "title": "Decide your offer",
                    "text": "Decide what you are promoting, such as a discount, special price, new product or limited-time offer."
                },
                {
                    "number": "1",
                    "title": "Choose a promotional template",
                    "text": "Search Canva for an offer, sale, promotion or announcement template that fits your message."
                },
                {
                    "number": "2",
                    "title": "Add the main offer",
                    "text": "Make the main offer clear and easy to notice, such as a percentage discount or special price."
                },
                {
                    "number": "3",
                    "title": "Add the product or service",
                    "text": "Clearly show which product or service is included in the promotion."
                },
                {
                    "number": "4",
                    "title": "Add the offer period",
                    "text": "If the offer has a specific start or end date, include the relevant dates clearly."
                },
                {
                    "number": "5",
                    "title": "Add a call-to-action",
                    "text": "Tell customers what they should do next, such as contact the business, visit the store or place an order."
                },
                {
                    "number": "6",
                    "title": "Add contact information",
                    "text": "Include an appropriate phone number, social media account, website or other method customers can use to contact the business."
                },
                {
                    "number": "7",
                    "title": "Review the promotion",
                    "text": "Check that the offer, dates, prices and contact information are accurate before sharing the design."
                }
            ],
            "activity": "Create a promotional graphic for a realistic small-business offer.",
            "visual": "activities/canva-offer-guide.png"
        },

        {
            "title": "Create Consistent Business Branding",
            "icon": "🏷️",
            "description": "Learn how to make your Canva designs look consistent by using the same business identity across different materials.",
            "steps": [
                {
                    "number": "0",
                    "title": "Collect your brand elements",
                    "text": "Prepare your business logo, preferred colours, business name and any commonly used fonts or design elements."
                },
                {
                    "number": "1",
                    "title": "Add your business logo",
                    "text": "Upload your logo to Canva and use it consistently in suitable designs."
                },
                {
                    "number": "2",
                    "title": "Choose your main colours",
                    "text": "Select a small set of colours that represent your business and use them consistently."
                },
                {
                    "number": "3",
                    "title": "Choose readable fonts",
                    "text": "Select fonts that are easy to read and suitable for your business style."
                },
                {
                    "number": "4",
                    "title": "Apply the same style",
                    "text": "Use similar colours, fonts, logo placement and visual style across your posters and social media designs."
                },
                {
                    "number": "5",
                    "title": "Compare your designs",
                    "text": "Place two or more designs side by side and check whether customers can recognise that they belong to the same business."
                },
                {
                    "number": "6",
                    "title": "Save and reuse your design",
                    "text": "Keep a copy of your successful design so you can reuse its structure for future business content."
                }
            ],
            "activity": "Create two different Canva designs that use the same business name, logo, colours and overall visual style.",
            "visual": "activities/canva-branding-guide.png"
        },

        {
            "title": "Download and Use Your Designs",
            "icon": "📥",
            "description": "Learn how to choose an appropriate file format, download your finished design and prepare it for use.",
            "steps": [
                {
                    "number": "0",
                    "title": "Finish your design",
                    "text": "Make sure the design is complete and that all text, images, prices and contact information are correct."
                },
                {
                    "number": "1",
                    "title": "Open the download option",
                    "text": "Use Canva's download or export option to prepare the finished design."
                },
                {
                    "number": "2",
                    "title": "Choose a file format",
                    "text": "Choose an appropriate format based on how you plan to use the design. Image formats are commonly useful for social media graphics."
                },
                {
                    "number": "3",
                    "title": "Download the file",
                    "text": "Download the completed design to your device and wait for the file to finish saving."
                },
                {
                    "number": "4",
                    "title": "Check the downloaded file",
                    "text": "Open the downloaded file and check that the design looks correct and that no important information is missing."
                },
                {
                    "number": "5",
                    "title": "Use the design for your business",
                    "text": "Use the finished design on the appropriate platform, such as Instagram, WhatsApp Business or printed promotional material."
                },
                {
                    "number": "6",
                    "title": "Keep an editable copy",
                    "text": "Keep your Canva design available so you can update prices, dates, products or other information later."
                }
            ],
            "activity": "Download one completed Canva design and prepare it for use on a social media platform.",
            "visual": "activities/canva-download-guide.png"
        }
    ],

    "activity": "Complete the Canva lessons in order. Create a business poster, an Instagram graphic, a promotional offer and a consistent branded design, then download one finished design for use.",

    "steps": [
        {
            "number": "0",
            "title": "Start with Canva",
            "text": "Create or sign in to Canva and learn how to find templates and open the design editor."
        },
        {
            "number": "1",
            "title": "Create your first business design",
            "text": "Follow the poster lesson and create a complete business design."
        },
        {
            "number": "2",
            "title": "Create social media content",
            "text": "Create an Instagram-ready graphic for a product or service."
        },
        {
            "number": "3",
            "title": "Create a promotional offer",
            "text": "Practise creating a design for a discount, offer or announcement."
        },
        {
            "number": "4",
            "title": "Build consistent branding",
            "text": "Create designs that use the same business logo, colours and visual style."
        },
        {
            "number": "5",
            "title": "Download and use your design",
            "text": "Finish the course by downloading a design and preparing it for real business use."
        }
    ],

    "visual": "activities/canva-guide.png"
},

"google-business": {
    "title": "Google Business Profile",
    "icon": "📍",
    "description": "Learn how to create, verify and manage a Google Business Profile so customers can find your business on Google Search and Maps.",

    "content": [
        {
            "heading": "Create or claim your profile",
            "text": "Learn how to add a new business to Google or claim an existing unverified Business Profile."
        },
        {
            "heading": "Add accurate business information",
            "text": "Learn how to add your business name, category, address or service area, phone number, website and opening hours."
        },
        {
            "heading": "Verify your business",
            "text": "Learn how Google verification works and how to complete the verification method offered for your business."
        },
        {
            "heading": "Build your online presence",
            "text": "Learn how to add photos, business information, updates and social links where available."
        },
        {
            "heading": "Manage customers and performance",
            "text": "Learn how to respond to reviews, keep information updated and understand available performance information."
        }
    ],

    "topics": [
        "Creating a Business Profile",
        "Claiming an existing profile",
        "Business name",
        "Business category",
        "Business address",
        "Service area",
        "Business hours",
        "Phone number",
        "Website",
        "Verification",
        "Business photos",
        "Customer reviews",
        "Business updates",
        "Performance and insights"
    ],

    "tips": [
        "Use your real business name and accurate business information.",
        "Choose the category that best represents what your business does.",
        "Keep your address or service area accurate.",
        "Keep business hours and contact details up to date.",
        "Only use genuine business photos and information.",
        "Never share Google verification codes with anyone.",
        "Respond to genuine customer reviews professionally.",
        "Keep access limited to people who actually need to manage the profile."
    ],

    "lessons": [
        {
            "title": "Create or Claim Your Business Profile",
            "icon": "🏪",
            "description": "Learn how to find out whether your business already has a Google Business Profile and how to add or claim it.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare before you begin",
                    "text": "Keep your business name, address or service area, phone number, website, business category and opening hours ready."
                },
                {
                    "number": "1",
                    "title": "Sign in to your Google Account",
                    "text": "Use the Google Account that you want to use to manage the business profile."
                },
                {
                    "number": "2",
                    "title": "Check whether your business already exists",
                    "text": "Search for your business name and location on Google Search or Google Maps to see whether a Business Profile already exists."
                },
                {
                    "number": "3",
                    "title": "Add your business if it is not listed",
                    "text": "If your business does not have a Business Profile, use Google's Business Profile setup to add the business and follow the on-screen instructions."
                },
                {
                    "number": "4",
                    "title": "Claim an existing business",
                    "text": "If an unverified profile already exists for your business, use the available claim option and follow Google's instructions to request management access."
                },
                {
                    "number": "5",
                    "title": "Check the business information",
                    "text": "Review the business name and other information before continuing. Make sure the information represents the real business accurately."
                },
                {
                    "number": "6",
                    "title": "Continue to verification",
                    "text": "Follow the setup process until Google shows the verification options available for your business."
                }
            ],
            "activity": "Find a real or sample business on Google Maps and determine whether it needs to be added or claimed.",
            "visual": "activities/google-business-account-guide.png"
        },

        {
            "title": "Add Your Business Information",
            "icon": "📝",
            "description": "Learn how to provide the important information customers need when they find your business on Google.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare accurate information",
                    "text": "Use information that accurately represents your real business and matches your real-world business presence."
                },
                {
                    "number": "1",
                    "title": "Add your business name",
                    "text": "Enter the business name as it is actually represented in the real world."
                },
                {
                    "number": "2",
                    "title": "Choose your primary category",
                    "text": "Choose the category that best describes the main activity of your business."
                },
                {
                    "number": "3",
                    "title": "Add your address or service area",
                    "text": "If customers visit your business location, provide the accurate address. If your business serves customers at their locations, use the appropriate service-area settings."
                },
                {
                    "number": "4",
                    "title": "Add your phone number",
                    "text": "Add an appropriate business phone number that customers can use to contact you."
                },
                {
                    "number": "5",
                    "title": "Add your website",
                    "text": "If your business has a website, add its complete web address to the profile."
                },
                {
                    "number": "6",
                    "title": "Set your business hours",
                    "text": "Add your normal opening hours and keep them updated when your schedule changes."
                },
                {
                    "number": "7",
                    "title": "Review your information",
                    "text": "Check the business name, category, location, contact details and hours before saving."
                }
            ],
            "activity": "Create a complete sample Business Profile using a fictional small business and enter all appropriate business information.",
            "visual": "activities/google-business-information-guide.png"
        },

        {
            "title": "Verify Your Business",
            "icon": "✅",
            "description": "Learn why verification is important and how to complete the verification method offered by Google.",
            "steps": [
                {
                    "number": "0",
                    "title": "Understand verification",
                    "text": "Verification helps Google confirm that you are authorised to represent and manage the business."
                },
                {
                    "number": "1",
                    "title": "Open your Business Profile",
                    "text": "Sign in to the Google Account associated with your Business Profile and open the profile."
                },
                {
                    "number": "2",
                    "title": "Select the available verification option",
                    "text": "Choose the verification method that Google makes available for your business. Options can vary by business and region."
                },
                {
                    "number": "3",
                    "title": "Follow Google's instructions",
                    "text": "Complete the steps shown for the selected verification method. Follow the instructions carefully."
                },
                {
                    "number": "4",
                    "title": "Keep verification information secure",
                    "text": "Never share verification codes or other security information with people who claim they need them to verify your business."
                },
                {
                    "number": "5",
                    "title": "Wait for verification to complete",
                    "text": "Google may review the information after you complete verification. Follow any additional instructions if Google requests them."
                },
                {
                    "number": "6",
                    "title": "Check your verified profile",
                    "text": "Once verification is complete, open your Business Profile and check that you can manage the business information."
                }
            ],
            "activity": "For a sample business, identify the verification process that would be required and list the information that should be kept ready.",
            "visual": "activities/google-business-verification-guide.png"
        },

        {
            "title": "Add Photos and Business Updates",
            "icon": "📸",
            "description": "Learn how to make your Business Profile more useful by adding genuine photos and keeping customers informed.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare genuine business photos",
                    "text": "Prepare clear photos that genuinely represent your business, such as the shop exterior, products, services or workspace."
                },
                {
                    "number": "1",
                    "title": "Open your Business Profile",
                    "text": "Sign in and open the Business Profile that you manage."
                },
                {
                    "number": "2",
                    "title": "Find the photo management option",
                    "text": "Use the available photo or media management controls to add images to your profile."
                },
                {
                    "number": "3",
                    "title": "Add your business photos",
                    "text": "Upload appropriate photos that help customers understand what your business looks like and what it offers."
                },
                {
                    "number": "4",
                    "title": "Add your logo or cover image where available",
                    "text": "Use suitable branding images where Google provides those options."
                },
                {
                    "number": "5",
                    "title": "Create a business update",
                    "text": "When the feature is available, create an update about an offer, event, announcement or useful business information."
                },
                {
                    "number": "6",
                    "title": "Review before publishing",
                    "text": "Check that your photos and update contain accurate information and do not include unnecessary private information."
                }
            ],
            "activity": "Prepare three genuine business photos and create a sample Google Business Profile update.",
            "visual": "activities/google-business-photos-guide.png"
        },

        {
            "title": "Manage Customer Reviews",
            "icon": "⭐",
            "description": "Learn how to read customer reviews and respond to them professionally.",
            "steps": [
                {
                    "number": "0",
                    "title": "Understand customer reviews",
                    "text": "Reviews provide customers with information about other people's experiences and give businesses feedback."
                },
                {
                    "number": "1",
                    "title": "Open your Business Profile",
                    "text": "Sign in to the Google Account that manages the Business Profile."
                },
                {
                    "number": "2",
                    "title": "Find your customer reviews",
                    "text": "Open the available reviews or customer feedback section of your Business Profile."
                },
                {
                    "number": "3",
                    "title": "Read the complete review",
                    "text": "Understand what the customer is saying before deciding how to respond."
                },
                {
                    "number": "4",
                    "title": "Reply professionally",
                    "text": "Thank customers for genuine positive feedback and provide a polite, useful response to concerns."
                },
                {
                    "number": "5",
                    "title": "Avoid sharing private information",
                    "text": "Do not reveal private customer information in a public response."
                },
                {
                    "number": "6",
                    "title": "Handle inappropriate reviews correctly",
                    "text": "If a review violates Google's policies, use the appropriate reporting or management options instead of responding aggressively."
                }
            ],
            "activity": "Write one professional response to a positive review and one professional response to a customer complaint.",
            "visual": "activities/google-business-reviews-guide.png"
        },

        {
            "title": "Understand Business Performance",
            "icon": "📊",
            "description": "Learn how to find available performance information and use it to understand customer interactions with your Business Profile.",
            "steps": [
                {
                    "number": "0",
                    "title": "Open your Business Profile",
                    "text": "Sign in to the Google Account that manages the profile and open the Business Profile."
                },
                {
                    "number": "1",
                    "title": "Find performance information",
                    "text": "Look for the available performance or insights section in your Business Profile. The available information can vary by profile and feature."
                },
                {
                    "number": "2",
                    "title": "Review customer interactions",
                    "text": "Look at the available information about how customers interact with your profile, such as searches, calls, website visits or other available actions."
                },
                {
                    "number": "3",
                    "title": "Identify useful patterns",
                    "text": "Look for patterns in the available information, such as increased customer activity after an update or a change in business information."
                },
                {
                    "number": "4",
                    "title": "Improve your profile",
                    "text": "Use what you learn to keep business information accurate and decide what content or updates may be useful for customers."
                },
                {
                    "number": "5",
                    "title": "Check your profile regularly",
                    "text": "Make profile management a regular task so that business information, photos, hours and customer interactions remain up to date."
                }
            ],
            "activity": "Review the available performance information for a sample or real Business Profile and identify three useful observations.",
            "visual": "activities/google-business-performance-guide.png"
        }
    ],

    "activity": "Complete the Google Business Profile lessons in order. Add or claim a business, enter accurate information, complete verification, add photos, practise responding to reviews and explore available performance information.",

    "steps": [
        {
            "number": "0",
            "title": "Create or claim your profile",
            "text": "Start by finding your business on Google or adding it if it is not already listed."
        },
        {
            "number": "1",
            "title": "Complete your business information",
            "text": "Add accurate business details including category, location, contact information and hours."
        },
        {
            "number": "2",
            "title": "Complete verification",
            "text": "Follow the verification method Google provides for your business."
        },
        {
            "number": "3",
            "title": "Add photos and updates",
            "text": "Make your profile useful and informative with genuine business photos and updates."
        },
        {
            "number": "4",
            "title": "Manage customer reviews",
            "text": "Read and respond to customer reviews professionally."
        },
        {
            "number": "5",
            "title": "Check performance",
            "text": "Explore the available performance information and use it to improve your profile."
        }
    ],

    "visual": "activities/google-business-guide.png"
},

    "ecommerce": {
    "title": "E-Commerce for Small Business",
    "icon": "🛒",
    "description": "Learn how to take a small business online, add products, manage orders, accept payments and promote an online store step by step.",

    "content": [
        {
            "heading": "Understand E-Commerce",
            "text": "Learn the basic idea of selling products or services online and identify what your business can offer."
        },
        {
            "heading": "Set up an Online Store",
            "text": "Learn how to choose a suitable selling platform and create the basic structure of an online store."
        },
        {
            "heading": "Add Products",
            "text": "Learn how to create product listings with names, descriptions, photos, prices and availability."
        },
        {
            "heading": "Manage Orders and Payments",
            "text": "Learn the basic process of receiving orders, accepting payments and preparing products for delivery."
        }
    ],

    "topics": [
        "Understanding E-Commerce",
        "Choosing products",
        "Identifying customers",
        "Choosing a selling platform",
        "Creating an online store",
        "Adding products",
        "Product photos",
        "Product descriptions",
        "Pricing",
        "Inventory",
        "Online payments",
        "Order management",
        "Delivery",
        "Customer service",
        "Store promotion",
        "Sales tracking"
    ],

    "tips": [
        "Start with a small number of products that you can manage properly.",
        "Use clear and genuine product photos.",
        "Write product descriptions that answer common customer questions.",
        "Keep prices and availability accurate.",
        "Clearly communicate delivery charges and expected delivery times.",
        "Use secure and trusted payment methods.",
        "Keep customer order and contact information private.",
        "Check your online store regularly for outdated information."
    ],

    "lessons": [
        {
            "title": "Understand E-Commerce and Choose What to Sell",
            "icon": "🧭",
            "description": "Learn the basics of online selling and decide what products or services your small business can offer online.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your business information",
                    "text": "Make a list of the products or services you offer, approximate prices, available stock or capacity and the customers you want to reach."
                },
                {
                    "number": "1",
                    "title": "Understand what E-Commerce means",
                    "text": "E-Commerce means buying and selling products or services using the internet. A small business can use an online store or other digital selling channels to reach customers."
                },
                {
                    "number": "2",
                    "title": "Choose what you want to sell online",
                    "text": "Select products or services that you can provide consistently and that are suitable for online selling."
                },
                {
                    "number": "3",
                    "title": "Identify your target customers",
                    "text": "Think about who is most likely to buy your products or services, including their needs, location and buying preferences."
                },
                {
                    "number": "4",
                    "title": "Prepare product information",
                    "text": "Collect product names, descriptions, photos, prices, sizes, colours, variations and other information customers may need."
                },
                {
                    "number": "5",
                    "title": "Decide where to sell",
                    "text": "Compare suitable options such as your own online store, an established marketplace or other appropriate digital selling channels."
                },
                {
                    "number": "6",
                    "title": "Plan your first online product list",
                    "text": "Choose a small group of products to start with instead of adding more products than you can manage."
                }
            ],
            "activity": "Create a sample list of five products or services that a small business could sell online and identify the target customer for each.",
            "visual": "activities/ecommerce-start-guide.png"
        },

        {
            "title": "Choose and Set Up an Online Store",
            "icon": "🏪",
            "description": "Learn the basic process of choosing an online selling platform and setting up the foundation of your store.",
            "steps": [
                {
                    "number": "0",
                    "title": "Decide what your store needs",
                    "text": "List the features your business needs, such as product listings, payments, delivery information, customer communication and order management."
                },
                {
                    "number": "1",
                    "title": "Compare suitable platforms",
                    "text": "Look at suitable online store or marketplace options and compare their features, costs, ease of use and suitability for your business."
                },
                {
                    "number": "2",
                    "title": "Create or sign in to your account",
                    "text": "Create an account on the platform you selected or sign in if you already have one."
                },
                {
                    "number": "3",
                    "title": "Enter your business information",
                    "text": "Add the business name and other basic information requested by the platform."
                },
                {
                    "number": "4",
                    "title": "Choose your store identity",
                    "text": "Add appropriate branding such as your business name, logo, colours and other available store information."
                },
                {
                    "number": "5",
                    "title": "Set basic store information",
                    "text": "Add relevant information such as business contact details, delivery areas, policies and other information required by the platform."
                },
                {
                    "number": "6",
                    "title": "Preview your store",
                    "text": "Check how your store appears to customers and make sure the basic information is understandable."
                }
            ],
            "activity": "Create a sample online-store setup plan including the platform, business name, contact information and basic store requirements.",
            "visual": "activities/ecommerce-store-guide.png"
        },

        {
            "title": "Add Your First Product",
            "icon": "📦",
            "description": "Learn how to create a complete product listing that gives customers the information they need before ordering.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your product information",
                    "text": "Keep the product name, clear photos, description, price, stock quantity and important product details ready."
                },
                {
                    "number": "1",
                    "title": "Open the product management area",
                    "text": "Open the store or marketplace dashboard and find the option used to add a new product."
                },
                {
                    "number": "2",
                    "title": "Enter the product name",
                    "text": "Use a clear product name that helps customers understand exactly what they are looking at."
                },
                {
                    "number": "3",
                    "title": "Add product photos",
                    "text": "Upload clear and genuine product photos from useful angles. Make sure the main product is easy to see."
                },
                {
                    "number": "4",
                    "title": "Write the product description",
                    "text": "Explain the important features, benefits, size, material, usage instructions or other details relevant to the product."
                },
                {
                    "number": "5",
                    "title": "Add the price",
                    "text": "Enter the correct selling price and clearly communicate any applicable offer or discount."
                },
                {
                    "number": "6",
                    "title": "Add availability or stock",
                    "text": "Enter the available stock or appropriate availability information if the platform provides this option."
                },
                {
                    "number": "7",
                    "title": "Choose the product category",
                    "text": "Place the product in the most appropriate category so customers can find it more easily."
                },
                {
                    "number": "8",
                    "title": "Review the product listing",
                    "text": "Check the product name, photos, description, price and availability before making the listing visible to customers."
                },
                {
                    "number": "9",
                    "title": "Publish the product",
                    "text": "Publish the product listing when all information is accurate. If the platform supports drafts, you can save it for later."
                }
            ],
            "activity": "Create a complete sample product listing with a product name, photo, description, price and availability.",
            "visual": "activities/ecommerce-product-guide.png"
        },

        {
            "title": "Set Up Delivery and Handle Orders",
            "icon": "🚚",
            "description": "Learn the basic process of receiving an online order, preparing it and communicating delivery information.",
            "steps": [
                {
                    "number": "0",
                    "title": "Plan your delivery method",
                    "text": "Decide whether you will deliver locally yourself, use a delivery service or use the delivery options provided by your selling platform."
                },
                {
                    "number": "1",
                    "title": "Define your delivery area",
                    "text": "Decide which locations your business can realistically serve."
                },
                {
                    "number": "2",
                    "title": "Set delivery charges",
                    "text": "Decide whether delivery is free, charged separately or included in the product price, depending on your business model."
                },
                {
                    "number": "3",
                    "title": "Receive an order",
                    "text": "Check your store or platform for new orders and review the customer's order details."
                },
                {
                    "number": "4",
                    "title": "Confirm the order",
                    "text": "Check the product, quantity, customer information and payment status before preparing the order."
                },
                {
                    "number": "5",
                    "title": "Prepare and pack the product",
                    "text": "Pack the product safely and appropriately for transport."
                },
                {
                    "number": "6",
                    "title": "Arrange delivery",
                    "text": "Hand the package to the selected delivery method and provide the necessary information."
                },
                {
                    "number": "7",
                    "title": "Update the order status",
                    "text": "Update the order status on your selling platform when the platform provides order-management options."
                },
                {
                    "number": "8",
                    "title": "Handle delivery problems",
                    "text": "Communicate clearly with the customer if there is a delay, stock issue or other genuine problem with the order."
                }
            ],
            "activity": "Create a sample order workflow from receiving an order to packing and delivering the product.",
            "visual": "activities/ecommerce-delivery-guide.png"
        },

        {
            "title": "Set Up and Manage Online Payments",
            "icon": "💳",
            "description": "Learn the basic process of accepting digital payments safely when selling online.",
            "steps": [
                {
                    "number": "0",
                    "title": "Understand your payment needs",
                    "text": "Decide which payment methods are appropriate for your customers and selling platform."
                },
                {
                    "number": "1",
                    "title": "Review available payment options",
                    "text": "Compare the payment methods supported by your store or marketplace, including their fees, availability and customer convenience."
                },
                {
                    "number": "2",
                    "title": "Choose a suitable payment method",
                    "text": "Select a trusted payment option that works with your selling platform and business requirements."
                },
                {
                    "number": "3",
                    "title": "Complete the payment setup",
                    "text": "Follow the payment provider or platform's official setup process and provide the required business information."
                },
                {
                    "number": "4",
                    "title": "Check payment confirmation",
                    "text": "Learn how your store indicates that a payment has been successfully completed before processing the order."
                },
                {
                    "number": "5",
                    "title": "Keep transaction records",
                    "text": "Maintain appropriate records of orders and payments so you can check your business transactions."
                },
                {
                    "number": "6",
                    "title": "Follow payment safety practices",
                    "text": "Never share passwords, PINs, OTPs or other confidential security information with customers or unknown people."
                }
            ],
            "activity": "Create a sample payment workflow showing how a customer places an order, makes a payment and receives confirmation.",
            "visual": "activities/ecommerce-payment-guide.png"
        },

        {
            "title": "Promote Your Online Store",
            "icon": "📣",
            "description": "Learn how to bring customers to your online store using social media and useful promotional content.",
            "steps": [
                {
                    "number": "0",
                    "title": "Choose a product to promote",
                    "text": "Select a product or service that you want to promote and prepare a clear photo and short description."
                },
                {
                    "number": "1",
                    "title": "Create promotional content",
                    "text": "Create a simple promotional graphic, photo, video or other useful content for your target customers."
                },
                {
                    "number": "2",
                    "title": "Add the product information",
                    "text": "Include the product name, important benefit, price or offer and a clear way to find or order the product."
                },
                {
                    "number": "3",
                    "title": "Share on Instagram",
                    "text": "Share suitable promotional content on your Instagram business profile and direct interested customers to the appropriate store or contact method."
                },
                {
                    "number": "4",
                    "title": "Share through WhatsApp Business",
                    "text": "Use appropriate WhatsApp Business communication to share products or offers with customers who have a legitimate reason to receive the information."
                },
                {
                    "number": "5",
                    "title": "Create an offer",
                    "text": "If appropriate, create a genuine limited-time offer or promotion with clear terms and dates."
                },
                {
                    "number": "6",
                    "title": "Track customer response",
                    "text": "Observe enquiries, visits, orders or other available responses to understand whether your promotion is reaching customers."
                }
            ],
            "activity": "Create a promotional campaign for one online product using a Canva graphic and an Instagram or WhatsApp Business message.",
            "visual": "activities/ecommerce-promotion-guide.png"
        },

        {
            "title": "Manage Orders and Improve Your Store",
            "icon": "📊",
            "description": "Learn how to review orders, customer feedback and store activity and use that information to improve your online business.",
            "steps": [
                {
                    "number": "0",
                    "title": "Review your store regularly",
                    "text": "Check your online store regularly to make sure product information, prices, stock and contact details are current."
                },
                {
                    "number": "1",
                    "title": "Check incoming orders",
                    "text": "Review new orders and make sure each order contains the information needed for processing."
                },
                {
                    "number": "2",
                    "title": "Track completed orders",
                    "text": "Keep track of orders that have been processed, delivered, cancelled or returned."
                },
                {
                    "number": "3",
                    "title": "Identify popular products",
                    "text": "Look at available sales information and identify products that receive more customer interest or orders."
                },
                {
                    "number": "4",
                    "title": "Review customer feedback",
                    "text": "Pay attention to customer questions, reviews and complaints to identify areas where the store or products can improve."
                },
                {
                    "number": "5",
                    "title": "Update products",
                    "text": "Update product photos, descriptions, prices or availability whenever the information changes."
                },
                {
                    "number": "6",
                    "title": "Improve your store",
                    "text": "Use what you learn from orders and customer feedback to improve your product listings, delivery process and promotional strategy."
                }
            ],
            "activity": "Review a sample online store and identify three changes that could make the store easier or more useful for customers.",
            "visual": "activities/ecommerce-management-guide.png"
        }
    ],

    "activity": "Complete the E-Commerce lessons in order. Choose products, plan an online store, create product listings, practise order and payment handling, promote a product and review store performance.",

    "steps": [
        {
            "number": "0",
            "title": "Understand what you want to sell",
            "text": "Identify your products, target customers and the information needed for online selling."
        },
        {
            "number": "1",
            "title": "Set up your online store",
            "text": "Choose an appropriate selling platform and create the basic store structure."
        },
        {
            "number": "2",
            "title": "Add your products",
            "text": "Create complete product listings with photos, descriptions, prices and availability."
        },
        {
            "number": "3",
            "title": "Manage delivery and payments",
            "text": "Learn the basic process of receiving orders, accepting payments and delivering products."
        },
        {
            "number": "4",
            "title": "Promote your store",
            "text": "Use suitable digital marketing channels to bring customers to your online products."
        },
        {
            "number": "5",
            "title": "Review and improve",
            "text": "Check orders, customer feedback and available sales information to improve your online store."
        }
    ],

    "visual": "activities/ecommerce-guide.png"
},

    "digital-payments": {
    "title": "Digital Payments for Small Business",
    "icon": "💳",
    "description": "Learn how to accept, check, record and manage digital payments safely in a small business.",

    "content": [
        {
            "heading": "Understand Digital Payments",
            "text": "Learn the basics of digital payments and common methods such as UPI, cards and bank transfers."
        },
        {
            "heading": "Set Up Business Payments",
            "text": "Learn how to choose an appropriate payment method and prepare it for accepting customer payments."
        },
        {
            "heading": "Accept Customer Payments",
            "text": "Learn how to receive payments, verify the transaction and confirm the correct amount."
        },
        {
            "heading": "Stay Safe",
            "text": "Learn important safety practices for protecting payment credentials and avoiding common payment scams."
        }
    ],

    "topics": [
        "Digital payment basics",
        "UPI",
        "QR payments",
        "Cards",
        "Bank transfers",
        "Business payment setup",
        "Accepting payments",
        "Checking transactions",
        "Payment records",
        "Refunds",
        "Failed payments",
        "Payment security",
        "Fraud awareness"
    ],

    "tips": [
        "Never share your UPI PIN, OTP, password or card security information.",
        "Receiving money does not require you to enter your UPI PIN.",
        "Always check your own payment app or bank account before confirming that money was received.",
        "Do not trust screenshots alone as proof of payment.",
        "Keep transaction records organised.",
        "Use only trusted and official payment applications and services.",
        "Check the recipient and amount carefully before approving a payment.",
        "Contact the payment provider or bank through official channels when a transaction looks suspicious."
    ],

    "lessons": [
        {
            "title": "Understand Digital Payments",
            "icon": "💡",
            "description": "Learn the basic types of digital payments and understand how they can be used by a small business.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your business payment needs",
                    "text": "Think about how customers currently pay your business and which digital payment methods could make payments easier."
                },
                {
                    "number": "1",
                    "title": "Understand digital payments",
                    "text": "Digital payments allow money to be transferred electronically without using physical cash."
                },
                {
                    "number": "2",
                    "title": "Learn about UPI",
                    "text": "UPI allows customers to make bank-account-based digital payments through supported payment applications and services."
                },
                {
                    "number": "3",
                    "title": "Understand QR payments",
                    "text": "A business can display an appropriate payment QR code so customers can scan it using a supported payment application."
                },
                {
                    "number": "4",
                    "title": "Understand card payments",
                    "text": "Customers may also pay using debit or credit cards through supported payment systems or payment terminals."
                },
                {
                    "number": "5",
                    "title": "Understand bank transfers",
                    "text": "Customers can sometimes transfer money directly to a business bank account using supported banking services."
                },
                {
                    "number": "6",
                    "title": "Choose suitable methods",
                    "text": "Consider your customers, business type, transaction needs and available services when deciding which payment methods to offer."
                }
            ],
            "activity": "Create a simple comparison of three digital payment methods that could be useful for a small business.",
            "visual": "activities/digital-payments-basics-guide.png"
        },

        {
            "title": "Set Up UPI for Business",
            "icon": "📱",
            "description": "Learn the general process of preparing a UPI-based payment method for accepting customer payments.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your requirements",
                    "text": "Keep the required bank-account, mobile-number and business information ready according to the official payment provider you choose."
                },
                {
                    "number": "1",
                    "title": "Choose an appropriate payment service",
                    "text": "Select a trusted UPI-enabled bank or payment service that supports the type of business payment setup you need."
                },
                {
                    "number": "2",
                    "title": "Complete the official setup",
                    "text": "Follow the provider's official instructions to connect or configure the appropriate payment account."
                },
                {
                    "number": "3",
                    "title": "Create or obtain the business QR",
                    "text": "If the service provides a business QR code, obtain it through the official application or provider process."
                },
                {
                    "number": "4",
                    "title": "Check the payment details",
                    "text": "Verify that the displayed business name or payment information is correct before using the QR code."
                },
                {
                    "number": "5",
                    "title": "Display the QR safely",
                    "text": "Place the QR code where genuine customers can easily see and scan it, while preventing unauthorised changes to the displayed payment information."
                },
                {
                    "number": "6",
                    "title": "Test the payment process",
                    "text": "Use a safe test transaction when appropriate and confirm that the payment appears correctly in your own payment account."
                }
            ],
            "activity": "Create a sample business payment setup plan showing the payment method, QR placement and payment-verification process.",
            "visual": "activities/digital-payments-upi-guide.png"
        },

        {
            "title": "Accept a Customer Payment",
            "icon": "🔳",
            "description": "Learn the practical process of accepting a digital payment and confirming that it was actually received.",
            "steps": [
                {
                    "number": "0",
                    "title": "Confirm the purchase amount",
                    "text": "Tell the customer the correct amount they need to pay before starting the payment."
                },
                {
                    "number": "1",
                    "title": "Show the payment option",
                    "text": "Provide the appropriate QR code, payment method or other supported payment option."
                },
                {
                    "number": "2",
                    "title": "Let the customer complete the payment",
                    "text": "Allow the customer to complete the payment using their own authorised payment application or method."
                },
                {
                    "number": "3",
                    "title": "Check your own payment account",
                    "text": "Check your own payment application, bank account or official transaction history to confirm whether the payment was received."
                },
                {
                    "number": "4",
                    "title": "Verify the amount",
                    "text": "Make sure the amount received matches the amount due."
                },
                {
                    "number": "5",
                    "title": "Confirm the transaction",
                    "text": "Once the payment is genuinely confirmed, complete the sale or provide the product or service."
                },
                {
                    "number": "6",
                    "title": "Record the payment",
                    "text": "Keep an appropriate business record of the sale and payment according to your business practice."
                }
            ],
            "activity": "Practise a sample digital-payment transaction and demonstrate how you would verify the payment before handing over a product.",
            "visual": "activities/digital-payments-payment-guide.png"
        },

        {
            "title": "Check and Record Transactions",
            "icon": "🧾",
            "description": "Learn how to check digital payment transactions and keep useful business records.",
            "steps": [
                {
                    "number": "0",
                    "title": "Understand why records matter",
                    "text": "Payment records help a business track sales, identify missing payments and organise financial information."
                },
                {
                    "number": "1",
                    "title": "Open your transaction history",
                    "text": "Use your official payment application, bank service or payment provider to view transaction information."
                },
                {
                    "number": "2",
                    "title": "Check the transaction status",
                    "text": "Look for the status of the transaction and make sure it has actually been completed before treating it as received."
                },
                {
                    "number": "3",
                    "title": "Check the amount",
                    "text": "Compare the amount received with the amount that the customer was expected to pay."
                },
                {
                    "number": "4",
                    "title": "Match the payment with the sale",
                    "text": "Connect the payment record with the relevant order, invoice or sale so the transaction can be identified later."
                },
                {
                    "number": "5",
                    "title": "Keep records organised",
                    "text": "Maintain appropriate records using a method suitable for your business, such as a spreadsheet, accounting system or other record-keeping method."
                },
                {
                    "number": "6",
                    "title": "Review records regularly",
                    "text": "Check your payment records regularly to identify missing, duplicate or unusual transactions."
                }
            ],
            "activity": "Create a sample transaction record containing date, order reference, amount, payment method and transaction status.",
            "visual": "activities/digital-payments-records-guide.png"
        },

        {
            "title": "Digital Payment Safety",
            "icon": "🔐",
            "description": "Learn the essential safety rules that every small business owner should follow when accepting digital payments.",
            "steps": [
                {
                    "number": "0",
                    "title": "Understand the basic safety rule",
                    "text": "Treat payment credentials and security information as private information that should never be shared with customers or strangers."
                },
                {
                    "number": "1",
                    "title": "Never share your UPI PIN",
                    "text": "Your UPI PIN is confidential. Never tell it to another person, even if they claim they need it to send you money."
                },
                {
                    "number": "2",
                    "title": "Never share OTPs",
                    "text": "Do not share one-time passwords or verification codes with customers, callers or unknown people."
                },
                {
                    "number": "3",
                    "title": "Do not trust screenshots alone",
                    "text": "A payment screenshot is not sufficient proof that money has reached your account. Check your own official transaction history."
                },
                {
                    "number": "4",
                    "title": "Understand payment requests",
                    "text": "Be careful when someone asks you to approve a payment request. Receiving money normally does not require you to enter your UPI PIN."
                },
                {
                    "number": "5",
                    "title": "Verify suspicious messages",
                    "text": "Do not open suspicious links or provide payment information in response to unexpected messages or calls."
                },
                {
                    "number": "6",
                    "title": "Use official support channels",
                    "text": "If something goes wrong, contact your bank or payment provider through its official website, application or customer-support channel."
                }
            ],
            "activity": "Identify five common digital-payment safety rules and create a small safety notice that could be displayed near a business payment counter.",
            "visual": "activities/digital-payments-safety-guide.png"
        },

        {
            "title": "Handle Refunds and Payment Problems",
            "icon": "↩️",
            "description": "Learn how to handle common payment problems such as failed, pending or incorrect transactions.",
            "steps": [
                {
                    "number": "0",
                    "title": "Identify the problem",
                    "text": "Determine whether the payment is failed, pending, duplicated, reversed, incorrect or genuinely completed."
                },
                {
                    "number": "1",
                    "title": "Check your own transaction history",
                    "text": "Check the official payment or bank account rather than relying only on the customer's message or screenshot."
                },
                {
                    "number": "2",
                    "title": "Ask the customer for relevant details",
                    "text": "When necessary, collect appropriate transaction information without asking for confidential PINs, passwords or OTPs."
                },
                {
                    "number": "3",
                    "title": "Check the provider's status",
                    "text": "Use the official payment application or bank service to understand the current transaction status."
                },
                {
                    "number": "4",
                    "title": "Follow the official refund process",
                    "text": "If a refund is required, use the payment provider, bank or selling platform's official refund procedure."
                },
                {
                    "number": "5",
                    "title": "Keep a record",
                    "text": "Record the relevant transaction and refund information so the issue can be followed up later."
                },
                {
                    "number": "6",
                    "title": "Communicate clearly with the customer",
                    "text": "Explain the status and next step politely without promising a result that you cannot confirm."
                }
            ],
            "activity": "Create a sample response for a customer whose payment is showing as pending and list the checks you would perform before taking further action.",
            "visual": "activities/digital-payments-refund-guide.png"
        },

        {
            "title": "Manage Digital Payments for Your Business",
            "icon": "📊",
            "description": "Learn how to organise digital payment activity and use payment information as part of everyday business management.",
            "steps": [
                {
                    "number": "0",
                    "title": "Review your payment methods",
                    "text": "List the digital payment methods your business currently accepts and identify whether each is still useful."
                },
                {
                    "number": "1",
                    "title": "Review transaction records",
                    "text": "Check your payment records and make sure they are organised and easy to understand."
                },
                {
                    "number": "2",
                    "title": "Match payments with sales",
                    "text": "Compare payment records with your orders or sales records to identify missing or unusual transactions."
                },
                {
                    "number": "3",
                    "title": "Identify common payment issues",
                    "text": "Look for repeated problems such as incorrect amounts, pending transactions or customer confusion."
                },
                {
                    "number": "4",
                    "title": "Improve the payment process",
                    "text": "Make payment instructions clearer and ensure customers know how to complete a payment safely."
                },
                {
                    "number": "5",
                    "title": "Review security practices",
                    "text": "Regularly remind anyone handling payments that PINs, OTPs, passwords and other security information must remain private."
                },
                {
                    "number": "6",
                    "title": "Make digital payments part of your routine",
                    "text": "Include payment checking and record-keeping in your normal daily or weekly business routine."
                }
            ],
            "activity": "Create a simple weekly digital-payment checklist for a small business.",
            "visual": "activities/digital-payments-management-guide.png"
        }
    ],

    "activity": "Complete the Digital Payments lessons in order. Understand payment methods, practise a sample UPI payment workflow, learn how to verify transactions, create safety rules and build a simple payment-record system.",

    "steps": [
        {
            "number": "0",
            "title": "Understand digital payments",
            "text": "Learn the common digital payment methods that can be useful for a small business."
        },
        {
            "number": "1",
            "title": "Prepare business payments",
            "text": "Choose an appropriate payment method and understand the general setup process."
        },
        {
            "number": "2",
            "title": "Accept and verify payments",
            "text": "Practise checking your own payment account before confirming a customer payment."
        },
        {
            "number": "3",
            "title": "Keep payment records",
            "text": "Learn how to organise transaction information and match payments with sales."
        },
        {
            "number": "4",
            "title": "Stay safe",
            "text": "Learn the most important rules for avoiding digital-payment fraud and protecting confidential information."
        },
        {
            "number": "5",
            "title": "Handle payment problems",
            "text": "Learn the basic process for dealing with pending, failed or refund-related payment issues."
        },
        {
            "number": "6",
            "title": "Manage payments regularly",
            "text": "Create a simple routine for checking and recording your business payments."
        }
    ],

    "visual": "activities/digital-payments-guide.png"
},

   "resources": {
    "title": "Digital Marketing Resources & Tips",
    "icon": "📚",
    "description": "Learn how to plan, create, promote and improve digital marketing activities for a small business using a simple step-by-step approach.",

    "content": [
        {
            "heading": "Know Your Customer",
            "text": "Understand who your customers are, what they need and which digital platforms they are most likely to use."
        },
        {
            "heading": "Set a Clear Goal",
            "text": "Choose a practical marketing goal such as increasing awareness, enquiries, website visits or sales."
        },
        {
            "heading": "Choose the Right Channels",
            "text": "Select digital platforms that match your business and where your target customers are active."
        },
        {
            "heading": "Create Useful Content",
            "text": "Create simple and useful posts, images, videos, offers and information that help customers understand your business."
        },
        {
            "heading": "Measure and Improve",
            "text": "Review your results, identify what worked and improve your next marketing activity."
        }
    ],

    "topics": [
        "Target customers",
        "Customer needs",
        "Marketing goals",
        "Digital channels",
        "Content planning",
        "Social media",
        "Google Business Profile",
        "WhatsApp Business",
        "Canva",
        "E-Commerce",
        "Digital payments",
        "Customer engagement",
        "Performance tracking",
        "Marketing improvement"
    ],

    "tips": [
        "Know your customer before deciding what content to create.",
        "Set one clear goal for each marketing activity.",
        "Choose platforms based on your customers, not simply on popularity.",
        "Use useful content instead of constantly advertising.",
        "Keep your business information consistent across platforms.",
        "Use genuine photos and accurate information.",
        "Respond professionally to customer questions and feedback.",
        "Track results and use them to improve future activities.",
        "Start with a manageable plan rather than trying to use every platform at once."
    ],

    "lessons": [
        {
            "title": "Identify Your Target Customer",
            "icon": "🎯",
            "description": "Learn how to identify the people most likely to need and buy your products or services.",
            "steps": [
                {
                    "number": "0",
                    "title": "Prepare your business information",
                    "text": "Write down what your business sells, the main benefits of your products or services and the type of customer you currently serve."
                },
                {
                    "number": "1",
                    "title": "Identify who buys from you",
                    "text": "Think about the people who already purchase your products or services and identify common characteristics."
                },
                {
                    "number": "2",
                    "title": "Understand customer needs",
                    "text": "Identify the problems, needs or goals that your product or service helps customers solve."
                },
                {
                    "number": "3",
                    "title": "Consider customer location",
                    "text": "Think about where your customers live or work and whether your business serves a local, regional or wider market."
                },
                {
                    "number": "4",
                    "title": "Consider customer interests",
                    "text": "Identify interests, habits or preferences that may help you create more relevant digital content."
                },
                {
                    "number": "5",
                    "title": "Create a simple customer profile",
                    "text": "Write a short description of your typical customer using the information you collected."
                },
                {
                    "number": "6",
                    "title": "Use the profile when planning marketing",
                    "text": "Use your customer profile to decide what to post, where to post it and what message will be most useful."
                }
            ],
            "activity": "Create a simple target-customer profile for a real or imaginary small business.",
            "visual": "activities/resources-customer-guide.png"
        },

        {
            "title": "Set a Digital Marketing Goal",
            "icon": "🎯",
            "description": "Learn how to choose a clear and practical goal for your digital marketing activity.",
            "steps": [
                {
                    "number": "0",
                    "title": "Identify the business problem",
                    "text": "Decide what you want to improve, such as low awareness, fewer enquiries, low website visits or low sales."
                },
                {
                    "number": "1",
                    "title": "Choose your main goal",
                    "text": "Choose one main goal for the marketing activity rather than trying to achieve everything at the same time."
                },
                {
                    "number": "2",
                    "title": "Choose an appropriate result to measure",
                    "text": "Decide what information can help you understand whether the activity is working, such as enquiries, visits, engagement or sales."
                },
                {
                    "number": "3",
                    "title": "Set a realistic target",
                    "text": "Choose a realistic target based on your current business situation and available resources."
                },
                {
                    "number": "4",
                    "title": "Set a time period",
                    "text": "Decide how long you will run the marketing activity before reviewing its results."
                },
                {
                    "number": "5",
                    "title": "Write your goal clearly",
                    "text": "Write the goal in one simple sentence so that you know exactly what you are trying to achieve."
                }
            ],
            "activity": "Create one digital marketing goal for a small business and define how you would measure its result.",
            "visual": "activities/resources-goal-guide.png"
        },

        {
            "title": "Choose the Right Digital Channels",
            "icon": "📱",
            "description": "Learn how to select digital platforms that are appropriate for your customers and business goals.",
            "steps": [
                {
                    "number": "0",
                    "title": "Review your target customer",
                    "text": "Use the customer profile from the previous lesson to think about where your customers are likely to look for information."
                },
                {
                    "number": "1",
                    "title": "Consider Instagram",
                    "text": "Instagram can be useful for businesses that benefit from visual content such as products, services, demonstrations and promotional designs."
                },
                {
                    "number": "2",
                    "title": "Consider WhatsApp Business",
                    "text": "WhatsApp Business can be useful for customer communication, enquiries, product information and business conversations."
                },
                {
                    "number": "3",
                    "title": "Consider Google Business Profile",
                    "text": "Google Business Profile can help customers discover eligible businesses through Google Search and Maps."
                },
                {
                    "number": "4",
                    "title": "Consider an online store",
                    "text": "An online store or suitable marketplace can be useful when customers need to browse products and place orders online."
                },
                {
                    "number": "5",
                    "title": "Choose your main channels",
                    "text": "Choose a manageable number of platforms that match your customers and your ability to maintain them regularly."
                },
                {
                    "number": "6",
                    "title": "Keep your information consistent",
                    "text": "Use consistent business names, contact information, branding and important business details across your chosen channels."
                }
            ],
            "activity": "Choose three digital channels for a sample business and explain why each one would be useful.",
            "visual": "activities/resources-channels-guide.png"
        },

        {
            "title": "Create a Simple Content Plan",
            "icon": "📝",
            "description": "Learn how to plan useful digital content instead of deciding what to post at the last minute.",
            "steps": [
                {
                    "number": "0",
                    "title": "Choose your content goal",
                    "text": "Decide what you want the content to achieve, such as informing customers, building trust, promoting a product or generating enquiries."
                },
                {
                    "number": "1",
                    "title": "Create product or service content",
                    "text": "Plan content that clearly shows what your business sells and explains its useful features or benefits."
                },
                {
                    "number": "2",
                    "title": "Create educational content",
                    "text": "Share useful tips, answers to common questions or information related to your products and services."
                },
                {
                    "number": "3",
                    "title": "Plan promotional content",
                    "text": "Create suitable content for offers, discounts, new products, events or other genuine business announcements."
                },
                {
                    "number": "4",
                    "title": "Include customer-focused content",
                    "text": "Where appropriate, share genuine customer feedback, frequently asked questions or useful customer experiences without exposing private information."
                },
                {
                    "number": "5",
                    "title": "Create a weekly schedule",
                    "text": "Choose realistic days and times for creating or publishing content based on what your business can consistently manage."
                },
                {
                    "number": "6",
                    "title": "Prepare content in advance",
                    "text": "Prepare photos, captions, graphics and other content before the planned publishing date whenever possible."
                }
            ],
            "activity": "Create a one-week content calendar containing at least five pieces of content for a sample small business.",
            "visual": "activities/resources-content-guide.png"
        },

        {
            "title": "Promote Your Business",
            "icon": "📣",
            "description": "Learn how to use the digital channels and content you created to reach potential customers.",
            "steps": [
                {
                    "number": "0",
                    "title": "Choose what to promote",
                    "text": "Select a product, service, useful piece of information or genuine offer that you want customers to notice."
                },
                {
                    "number": "1",
                    "title": "Prepare your promotional content",
                    "text": "Use appropriate photos, videos, Canva designs or other content to communicate the message clearly."
                },
                {
                    "number": "2",
                    "title": "Write a clear message",
                    "text": "Explain what you are offering and why it may be useful to the customer."
                },
                {
                    "number": "3",
                    "title": "Add a call-to-action",
                    "text": "Tell customers what they can do next, such as visit the store, send an enquiry, view a product or place an order."
                },
                {
                    "number": "4",
                    "title": "Publish on the appropriate channel",
                    "text": "Share the content on the digital platform that matches your target customer and marketing goal."
                },
                {
                    "number": "5",
                    "title": "Avoid spam",
                    "text": "Do not repeatedly send unwanted promotional messages. Focus on useful and relevant communication."
                },
                {
                    "number": "6",
                    "title": "Respond to interested customers",
                    "text": "Check comments and enquiries and provide useful, professional responses."
                }
            ],
            "activity": "Create one promotional campaign using a Canva design and choose an appropriate digital channel for publishing it.",
            "visual": "activities/resources-promotion-guide.png"
        },

        {
            "title": "Track Your Results",
            "icon": "📊",
            "description": "Learn how to check whether your digital marketing activities are reaching customers and producing useful results.",
            "steps": [
                {
                    "number": "0",
                    "title": "Return to your original goal",
                    "text": "Look at the goal you set and identify which results will help you decide whether the activity was useful."
                },
                {
                    "number": "1",
                    "title": "Check available platform information",
                    "text": "Review the available insights, analytics or performance information on the digital platforms you use."
                },
                {
                    "number": "2",
                    "title": "Check customer engagement",
                    "text": "Look at useful indicators such as comments, messages, enquiries, shares or other available engagement information."
                },
                {
                    "number": "3",
                    "title": "Check business actions",
                    "text": "Where available, review actions such as website visits, product views, calls, orders or other meaningful customer actions."
                },
                {
                    "number": "4",
                    "title": "Compare with your goal",
                    "text": "Compare the results with the target you originally set."
                },
                {
                    "number": "5",
                    "title": "Identify what worked",
                    "text": "Identify the content, channel or approach that produced useful results."
                },
                {
                    "number": "6",
                    "title": "Record your findings",
                    "text": "Write down the main results so you can compare them with future marketing activities."
                }
            ],
            "activity": "Create a simple results sheet containing your marketing goal, activity, important metrics and observations.",
            "visual": "activities/resources-results-guide.png"
        },

        {
            "title": "Improve Your Digital Marketing Strategy",
            "icon": "🔄",
            "description": "Learn how to use your results to improve the next round of digital marketing activities.",
            "steps": [
                {
                    "number": "0",
                    "title": "Review what you learned",
                    "text": "Look at the results and observations from your previous marketing activity."
                },
                {
                    "number": "1",
                    "title": "Keep what worked",
                    "text": "Identify successful approaches that are practical for your business and consider using them again."
                },
                {
                    "number": "2",
                    "title": "Identify what needs improvement",
                    "text": "Look for content, platforms or approaches that did not produce useful results."
                },
                {
                    "number": "3",
                    "title": "Change one or two things",
                    "text": "Make practical improvements rather than changing everything at once, so you can understand what makes a difference."
                },
                {
                    "number": "4",
                    "title": "Create the next content plan",
                    "text": "Use what you learned to prepare your next set of digital marketing activities."
                },
                {
                    "number": "5",
                    "title": "Set the next goal",
                    "text": "Choose another clear and realistic goal for your next marketing period."
                },
                {
                    "number": "6",
                    "title": "Repeat the improvement cycle",
                    "text": "Continue the cycle of planning, creating, publishing, measuring and improving your digital marketing activities."
                }
            ],
            "activity": "Create a one-month improvement plan showing what you will continue, what you will change and what you will measure.",
            "visual": "activities/resources-improvement-guide.png"
        }
    ],

    "activity": "Complete the Digital Marketing Resources lessons from beginning to end. Identify your customer, set a goal, choose channels, create a content plan, promote your business, measure the results and prepare your next marketing plan.",

    "steps": [
        {
            "number": "0",
            "title": "Identify your target customer",
            "text": "Understand who your business wants to reach and what those customers need."
        },
        {
            "number": "1",
            "title": "Set a marketing goal",
            "text": "Choose one clear result that you want your digital marketing activity to achieve."
        },
        {
            "number": "2",
            "title": "Choose digital channels",
            "text": "Select manageable platforms that match your customers and business."
        },
        {
            "number": "3",
            "title": "Create a content plan",
            "text": "Plan useful, promotional and customer-focused content for the coming days or weeks."
        },
        {
            "number": "4",
            "title": "Promote your business",
            "text": "Publish relevant content and communicate with interested customers."
        },
        {
            "number": "5",
            "title": "Track your results",
            "text": "Review useful performance information and compare it with your original goal."
        },
        {
            "number": "6",
            "title": "Improve your strategy",
            "text": "Use your results to improve the next marketing plan and continue the cycle."
        }
    ],

    "visual": "activities/resources-guide.png"
}
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/training")
def training():
    return render_template("training.html", modules=MODULES)


@app.route("/module/<slug>", methods=["GET", "POST"])
def module(slug):
    data = MODULES.get(slug)
    if not data:
        return render_template("404.html"), 404
    progress = ModuleProgress.query.filter_by(module_slug=slug).first()
    if not progress:
        progress = ModuleProgress(module_slug=slug, title=data["title"], views=1)
        db.session.add(progress)
    else:
        progress.views += 1
    db.session.commit()
    return render_template("module.html", module=data, slug=slug)


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        try:
            response = SurveyResponse(
                survey_type=request.form["survey_type"],
                name=request.form["name"].strip(),
                business=request.form["business"].strip(),
                platform=request.form["platform"],
                confidence=int(request.form["confidence"]),
                online_presence=int(request.form["online_presence"]),
                challenges=request.form["challenges"].strip(),
                feedback=request.form.get("feedback", "").strip()
            )
            db.session.add(response)
            db.session.commit()
            flash("Thank you! Your survey response has been saved.", "success")
            return redirect(url_for("survey"))
        except (KeyError, ValueError):
            flash("Please complete all required survey fields.", "error")
    return render_template("survey.html")


def average(rows, field):
    return round(sum(getattr(r, field) for r in rows) / len(rows), 1) if rows else 0


@app.route("/results")
def results():
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.asc()).all()
    pre = [r for r in responses if r.survey_type == "pre"]
    post = [r for r in responses if r.survey_type == "post"]
    stats = {
        "total": len(responses),
        "pre": len(pre),
        "post": len(post),
        "pre_confidence": average(pre, "confidence"),
        "post_confidence": average(post, "confidence"),
        "pre_presence": average(pre, "online_presence"),
        "post_presence": average(post, "online_presence")
    }
    stats["confidence_change"] = round(stats["post_confidence"] - stats["pre_confidence"], 1) if pre and post else 0
    stats["presence_change"] = round(stats["post_presence"] - stats["pre_presence"], 1) if pre and post else 0
    return render_template("results.html", stats=stats)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.desc()).all()
    contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    module_rows = ModuleProgress.query.order_by(ModuleProgress.views.desc()).all()

    pre = [r for r in responses if r.survey_type == "pre"]
    post = [r for r in responses if r.survey_type == "post"]

    platforms = ["Instagram", "Facebook", "WhatsApp Business", "Google Business Profile", "None yet", "Other"]
    platform_counts = {platform: sum(r.platform == platform for r in responses) for platform in platforms}

    challenge_counts = {}
    for response in responses:
        challenge = response.challenges.strip() or "Not specified"
        challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
    top_challenges = sorted(challenge_counts.items(), key=lambda item: (-item[1], item[0]))[:6]

    stats = {
        "total": len(responses),
        "pre": len(pre),
        "post": len(post),
        "contacts": len(contacts),
        "pre_confidence": average(pre, "confidence"),
        "post_confidence": average(post, "confidence"),
        "pre_presence": average(pre, "online_presence"),
        "post_presence": average(post, "online_presence"),
        "module_views": sum(m.views for m in module_rows)
    }

    chart_data = {
        "confidence": [stats["pre_confidence"], stats["post_confidence"]],
        "presence": [stats["pre_presence"], stats["post_presence"]],
        "platform_labels": list(platform_counts.keys()),
        "platform_values": list(platform_counts.values())
    }

    return render_template(
        "admin.html",
        stats=stats,
        responses=responses,
        contacts=contacts,
        module_rows=module_rows,
        top_challenges=top_challenges,
        chart_data=chart_data
    )


@app.route("/admin/export/surveys")
def export_surveys():
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Survey Type", "Name", "Business", "Platform",
        "Confidence", "Online Presence", "Challenges", "Feedback", "Created At"
    ])
    for r in responses:
        writer.writerow([
            r.id, r.survey_type, r.name, r.business, r.platform,
            r.confidence, r.online_presence, r.challenges, r.feedback or "",
            r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
        ])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=digigrow_survey_results.csv"}
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not all(request.form.get(k, "").strip() for k in ["name", "email", "message"]):
            flash("Please fill in all contact fields.", "error")
        else:
            db.session.add(ContactMessage(
                name=request.form["name"].strip(),
                email=request.form["email"].strip(),
                message=request.form["message"].strip()
            ))
            db.session.commit()
            flash("Your message has been received. Thank you!", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/api/stats")
def api_stats():
    responses = SurveyResponse.query.all()
    return jsonify({
        "survey_responses": len(responses),
        "pre_training": sum(r.survey_type == "pre" for r in responses),
        "post_training": sum(r.survey_type == "post" for r in responses),
        "module_views": sum(m.views for m in ModuleProgress.query.all())
    })

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.context_processor
def inject_globals():
    return {"year": datetime.now().year, "modules": MODULES}


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DigiGrow database initialized.")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
