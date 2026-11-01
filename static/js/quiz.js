document.addEventListener("DOMContentLoaded", () => {
    const section = document.getElementById("module-quiz");

    if (!section) return;

    const slug = section.dataset.moduleSlug;

    // 10 questions for each training module
    const quizzes = {
        "social-media": [
            ["What is a business social profile for?", ["Help customers discover the business", "Store private passwords", "Replace product quality", "Avoid customer contact"], 0, "It helps people find the business."],
            ["What should an Instagram bio include?", ["Business name and offer", "Only random quotes", "Customer PINs", "Unrelated jokes"], 0, "A clear bio explains the business and how to contact it."],
            ["What is a useful social media post?", ["Helpful product or service information", "Repeated blank images", "Private customer data", "Unrelated spam"], 0, "Useful content helps customers understand the business."],
            ["What are Instagram Reels?", ["Short-form videos", "Bank statements", "Text-only invoices", "Business licences"], 0, "Reels are short videos suitable for demonstrations and promotions."],
            ["What is social media engagement?", ["Likes, comments, shares and saves", "Shop rent", "Product stock only", "Internet bill"], 0, "Engagement describes how people interact with content."],
            ["Why use clear product photos?", ["Help customers understand the product", "Guarantee every sale", "Replace all descriptions", "Hide product details"], 0, "Clear photos make products easier to understand."],
            ["What is a good posting habit?", ["Publish useful content consistently", "Post unrelated content every minute", "Never reply", "Change the profile daily"], 0, "A realistic schedule keeps the profile useful."],
            ["How should a business answer questions?", ["Politely and accurately", "With abusive language", "Ask for passwords", "Ignore every customer"], 0, "Professional replies build trust."],
            ["What should an offer clearly show?", ["Terms and dates", "Hidden conditions", "False prices", "Customer OTPs"], 0, "Clear terms help customers understand the offer."],
            ["How can a business review a post?", ["Check reach, interactions and enquiries", "Check phone wallpaper", "Count shop chairs", "Ignore results"], 0, "These measures help understand content performance."]
        ],

        "canva": [
            ["What is Canva used for?", ["Creating visual designs", "Managing bank accounts", "Tracking parcels", "Writing drivers"], 0, "Canva is a tool for graphics and presentations."],
            ["What is a template?", ["A ready-made layout to customise", "A bank receipt", "A password", "A business licence"], 0, "Templates provide a starting point for a design."],
            ["What should you do with a template?", ["Customise text, images and colours", "Use without checking", "Delete all details", "Share your password"], 0, "Customising makes the design suitable for your business."],
            ["Why use consistent colours and fonts?", ["Build a recognisable visual identity", "Make text unreadable", "Hide the business name", "Reduce product quality"], 0, "Consistent styles help customers recognise a brand."],
            ["What is suitable for a product promotion?", ["A clear product graphic", "A blank page", "Private messages", "An unrelated document"], 0, "A graphic can show the product and its details."],
            ["What should you check before downloading?", ["Spelling, image quality and layout", "Only file name", "Phone battery", "Unrelated comments"], 0, "A final review catches mistakes."],
            ["Why resize a design?", ["Fit a platform or format", "Change bank details", "Remove all text", "Increase internet speed"], 0, "Different platforms may need different dimensions."],
            ["What should a business poster contain?", ["Clear message and contact or offer details", "Private customer data", "Hidden business name", "Unrelated paragraphs"], 0, "A poster should communicate clearly."],
            ["What is a good image-use practice?", ["Use relevant images you have permission to use", "Copy any image without checking", "Use blurry images", "Use unrelated images"], 0, "Use relevant images and respect permissions."],
            ["What should you do before sharing a design?", ["Export suitably and review it", "Share your password", "Remove key information", "Publish without checking"], 0, "Reviewing the design helps ensure it displays correctly."]
        ],

        "google-business": [
            ["What is Google Business Profile for?", ["Managing business appearance on Search and Maps", "Making games", "Editing videos", "Sending bank transfers"], 0, "It helps customers find business information on Google."],
            ["Which details should be accurate?", ["Name, address, phone and hours", "Customer PIN", "Competitor passwords", "Unrelated photos"], 0, "Correct details help customers contact or visit."],
            ["Why choose the correct category?", ["Describe the type of business", "Change bank balance", "Guarantee first rank", "Hide location"], 0, "A relevant category helps explain the business."],
            ["Why add clear photos?", ["Show the business, products or services", "Replace the address", "Hide opening hours", "Stop all questions"], 0, "Photos help customers know what to expect."],
            ["What if opening hours change?", ["Update the profile", "Keep old hours forever", "Delete reviews", "Change category randomly"], 0, "Current hours prevent customer confusion."],
            ["How respond to a genuine review?", ["Politely and professionally", "Share reviewer password", "Use abusive language", "Ignore every review"], 0, "Professional responses show that feedback matters."],
            ["What is a review link for?", ["Help customers leave a review", "Change bank details", "Create a barcode", "Edit hours automatically"], 0, "It gives customers a direct way to review."],
            ["What should businesses avoid?", ["Fake reviews", "Politely asking genuine customers", "Good service", "Respectful replies"], 0, "Reviews should reflect real customer experiences."],
            ["Why verify a profile?", ["Confirm authorised profile management", "Guarantee unlimited sales", "Remove customer service", "Access private accounts"], 0, "Verification helps confirm control of the profile."],
            ["What can profile insights show?", ["How customers find and interact with the profile", "Visitor passwords", "Competitor bank data", "Private messages"], 0, "Insights show discovery and customer actions."]
        ],

        "ecommerce": [
            ["What is e-commerce?", ["Buying and selling online", "Only physical shop sales", "Repairing computers", "Printing cards"], 0, "E-commerce is buying and selling through electronic networks."],
            ["What should a product listing include?", ["Name, photos, description, price and availability", "Only emoji", "Customer password", "Unrelated news"], 0, "Customers need clear product information."],
            ["Why use clear product photos?", ["Help customers see the product", "Guarantee delivery", "Confirm payment", "Replace all details"], 0, "Photos help customers understand the product."],
            ["What should be checked for a new order?", ["Product, quantity, customer details and payment status", "Profile picture only", "Shop wall colour", "Social likes"], 0, "Checking details prevents fulfilment mistakes."],
            ["Why define a delivery area?", ["Set locations the business can serve", "Change product quality", "Remove records", "Create followers"], 0, "A realistic delivery area sets expectations."],
            ["What before publishing a listing?", ["Review details for accuracy", "Leave price blank", "Use unrelated photo", "Show incorrect stock"], 0, "Reviewing keeps the listing accurate."],
            ["How promote an online store?", ["Share relevant content on suitable channels", "Hide the store link", "Send unwanted spam", "Never describe products"], 0, "Relevant promotion can attract interested customers."],
            ["Why update stock information?", ["Show whether products are available", "Speed up website", "Hide charges", "Replace support"], 0, "Accurate availability reduces confusion."],
            ["What if an order is delayed?", ["Communicate clearly with the customer", "Pretend it arrived", "Delete the order", "Ask for OTP"], 0, "Clear communication manages expectations."],
            ["How improve an online store?", ["Review orders and feedback, then improve", "Ignore all feedback", "Remove product info", "Stop checking stock"], 0, "Orders and feedback identify areas to improve."]
        ],

        "digital-payments": [
            ["What is a digital payment?", ["Electronic transfer of money", "Shopping list", "Paper advertisement", "Product photo"], 0, "Digital payments transfer money electronically."],
            ["Which is a digital payment method?", ["UPI", "Paper poster", "Printed menu", "Product label"], 0, "UPI is a common electronic payment method."],
            ["What is used for a QR payment?", ["Supported payment app", "Photo editor", "Word processor", "Music player"], 0, "A supported payment app scans the business QR code."],
            ["How confirm a payment was received?", ["Check own official payment app or bank account", "Trust screenshot alone", "Ask for OTP", "Assume success"], 0, "Verify the transaction in your own account."],
            ["Should you share your UPI PIN?", ["No, keep it confidential", "Yes, if asked", "Over phone only", "Print it on QR"], 0, "A UPI PIN must remain private."],
            ["Does receiving money normally require your UPI PIN?", ["No", "Yes, always", "Only with screenshot", "Only for small payments"], 0, "A PIN is generally used to authorise sending money."],
            ["Why keep transaction records?", ["Track payments and match sales", "Share credentials", "Avoid verification", "Replace listings"], 0, "Records help track and review transactions."],
            ["What if a payment is pending?", ["Check official status and provider guidance", "Assume success", "Ask customer PIN", "Send product without checking"], 0, "Pending transactions need verification."],
            ["What if you suspect a payment scam?", ["Contact bank/provider through official channels", "Click every link", "Share OTP", "Ignore alerts"], 0, "Official support channels are safer."],
            ["How process a refund?", ["Use official provider or platform procedure", "Ask for password", "Share UPI PIN", "Use unknown link"], 0, "Refunds should follow official procedures."]
        ],

        "resources": [
            ["Why identify target customers?", ["Understand who to reach and their needs", "Copy competitors", "Avoid planning", "Hide products"], 0, "Knowing customers guides content and channel choices."],
            ["Which is a practical marketing goal?", ["Increase relevant customer enquiries", "Post without purpose", "Change logo hourly", "Avoid measurement"], 0, "A clear goal gives marketing a direction."],
            ["How choose marketing channels?", ["Choose platforms used by target customers", "Choose randomly", "Use all platforms regardless", "Ignore preferences"], 0, "Channel choice depends on the audience and business."],
            ["What makes content useful?", ["Answers questions or explains products clearly", "Unrelated slogans", "Hides contact details", "Repeats without purpose"], 0, "Useful content helps customers make informed decisions."],
            ["Why create a content plan?", ["Organise what to publish and when", "Stop communication", "Remove goals", "Guarantee viral reach"], 0, "A plan supports consistent purposeful publishing."],
            ["What after reviewing campaign results?", ["Identify what worked and improve", "Ignore results", "Delete content", "Stop serving customers"], 0, "Results guide future decisions."],
            ["Which metric can show interest?", ["Enquiries or clicks", "Shoe size", "Number of chairs at home", "Wallpaper"], 0, "Enquiries and clicks can show audience response."],
            ["Why use a call to action?", ["Tell customers the next step", "Confuse visitors", "Hide contact details", "Replace product info"], 0, "A call to action guides visitors to act."],
            ["How improve a weak campaign?", ["Review audience, message and results", "Spend without checking", "Repeat forever unchanged", "Stop recording"], 0, "Evidence-based changes can improve campaigns."],
            ["Which is a good marketing habit?", ["Plan, publish, respond and review regularly", "Publish once and forget", "Ignore questions", "Use misleading offers"], 0, "Regular planning and review support improvement."]
        ]
    };

    const questions = quizzes[slug];

    const startPanel = document.getElementById("quiz-start");
    const startButton = document.getElementById("start-quiz");
    const form = document.getElementById("quiz-form");
    const list = document.getElementById("quiz-questions");
    const result = document.getElementById("quiz-result");

    if (!questions) {
        startPanel.innerHTML =
            "<p>Quiz not available for this module. Check the module slug.</p>";
        return;
    }

function renderQuestions() {
    list.innerHTML = questions.map((q, i) => {

        // Create options with their original indexes
        const shuffledOptions = q[1]
            .map((option, originalIndex) => ({
                text: option,
                index: originalIndex
            }))
            .sort(() => Math.random() - 0.5);

        return `
            <section class="quiz-question">
                <h3>${i + 1}. ${q[0]}</h3>

                ${shuffledOptions.map(option => `
                    <label class="quiz-option">
                        <input
                            type="radio"
                            name="question-${i}"
                            value="${option.index}"
                            required
                        >
                        ${option.text}
                    </label>
                `).join("")}
            </section>
        `;
    }).join("");
}

    // Start quiz
    startButton.addEventListener("click", () => {
        renderQuestions();

        startPanel.hidden = true;
        result.hidden = true;
        form.hidden = false;

        form.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });

    // Submit quiz and calculate score
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        let score = 0;

        const review = questions.map((q, i) => {
            const selected = Number(
                form.querySelector(
                    `input[name="question-${i}"]:checked`
                ).value
            );

            const correct = selected === q[2];

            if (correct) score++;

            return `
                <section class="quiz-question">
                    <h3>${i + 1}. ${q[0]}</h3>

                    <p class="${correct ? "quiz-correct" : "quiz-wrong"}">
                        ${correct ? "Correct" : "Incorrect"}
                        — Correct answer: ${q[1][q[2]]}
                    </p>

                    <p>${q[3]}</p>
                </section>
            `;
        }).join("");

        const percentage = Math.round(
            (score / questions.length) * 100
        );

        form.hidden = true;
        result.hidden = false;

        result.innerHTML = `
            <div class="quiz-result">

                <h3>Your Quiz Result</h3>

                <p>
                    <strong>
                        ${score} / ${questions.length} correct
                    </strong>
                </p>

                <p><strong>${percentage}%</strong></p>

                <p>
                    ${
                        percentage >= 80
                            ? "Excellent work! You have a strong understanding of this module."
                            : percentage >= 50
                            ? "Good effort! Review the explanations and try again."
                            : "Keep learning. Review the lessons and retake the quiz."
                    }
                </p>

                <div class="quiz-review">
                    ${review}
                </div>

                <button
                    type="button"
                    class="btn primary"
                    id="retake-quiz"
                >
                    Retake Quiz ↻
                </button>

            </div>
        `;

        // Retake quiz
        document.getElementById("retake-quiz")
            .addEventListener("click", () => {

                form.reset();
                result.hidden = true;
                form.hidden = true;
                startPanel.hidden = false;

                startPanel.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            });

        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
});