
# Example usage:
letter_content = """
Hey there

Check out this cool website: https://example.com and also this one www.another-example.com.\n
helllo mwoww mwoeeowdsads ksajddsai ate sweets dsajkhfjashfasf '\n'

jsakdhlsaflsajkfl sfajfkls afklsafklsajfhlk saf
sahflksahflhsafla 


Don't forget to visit http://test.com as well.
Let's talk about it later!

Best,
Your Friend
"""

# para = process_letter_content(letter_content)



def process_links(content):
    # List of known URL schemes to check
    url_schemes = ["http://", "https://", "www."]
    
    # Split the content into paragraphs
    paragraphs = content.split("\n")
    
    # Initialize lists for links and normal paragraphs
    links = []
    normal_paragraphs = []

    # Iterate through each paragraph
    for para in paragraphs:
        # Split the paragraph into words
        words = para.split()
        
        # Initialize a temporary list for non-link words
        non_link_words = []
        
        # Check each word to see if it's a link
        for word in words:
            if any(word.startswith(scheme) for scheme in url_schemes):
                links.append(word)  # If a link, add to the links list
            else:
                non_link_words.append(word)  # Otherwise, keep it as part of the normal paragraph
        
        # Rebuild the paragraph from non-link words
        if non_link_words:
            normal_paragraphs.append(" ".join(non_link_words))
    
    return normal_paragraphs, links


para, links = process_links(letter_content)
print(para)
print(links)









# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, MultipleFileField, EmailField
# from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
# from flask_wtf.file import FileField, FileAllowed



# class WriteForm(FlaskForm):
    
#     receiver = SelectField('Select receiver', validators=[DataRequired()],  render_kw={"placeholder": "Who are you sending?"})
#     def validate_receiver(form, field):
#         if field.data == '':
#             raise ValidationError('Please select a valid partner as the receiver.')
#     title = StringField('Title..',
#                 validators=[DataRequired(),Length(min = 3, max= 40 )], render_kw={"placeholder": "Title"})
#     content = TextAreaField( 
#             validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
#     # content = CKEditorField('write your letter here :)',validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
   
#     images = MultipleFileField('Your images', validators=[FileAllowed(['jpg', 'png', 'gif','jpeg'], 'Images only!')],render_kw={"placeholder": "Add Images?"})
 

#     submit = SubmitField('Send >')
    
   
   
# words= """## The Nine Lives of Fascination: Unraveling the Enigma of the Cat

# Cats, with their enigmatic gaze and independent spirit, have captivated humanity for millennia. From the revered deities of ancient Egypt to the internet's reigning meme lords, these furry enigmas hold a unique place in our hearts and homes. But what is it about these feline companions that continues to fascinate us?

# One aspect of their allure lies in their inherent duality. They are both fiercely independent hunters, capable of bringing down prey ten times their size, and cuddly lap warmers, purring contentedly on their humans' laps. This seemingly contradictory nature fuels our curiosity, prompting us to decipher their meows, decipher their tail flicks, and understand the complex motivations behind their every pounce and swat.

# Their sensory prowess adds another layer to the mystery. With eyes attuned to the faintest light and ears that can detect the subtlest sounds, they seem to navigate a world unseen by us. This heightened awareness fuels the perception of cats as mystical creatures, capable of sensing hidden energies and guarding unseen portals.

# But while their aloofness may contribute to their enigmatic aura, it's equally important to recognize the profound bond cats can form with their human companions. Studies have shown that owning a cat can lower stress levels, reduce loneliness, and even improve cardiovascular health. The unconditional love and purring presence they offer can provide solace and comfort in a way no other creature can.

# Beyond the individual level, cats have played significant roles in human history and culture. From their role as vermin control in ancient Egypt to their symbolic representation in various mythologies, they have left their paw prints on the tapestry of human experience. Their enduring popularity in art, literature, and even social media solidifies their place in our collective imagination.

# However, our fascination with cats is not without its complexities. The rise of "cat culture" on the internet, while undeniably entertaining, can sometimes trivialize their needs and promote harmful stereotypes. It's crucial to remember that these are sentient beings, deserving of respect and responsible care.

# As we continue to unravel the mysteries of the feline world, it's important to appreciate them not just for their cuteness or meme-worthiness, but for the complex creatures they truly are. By understanding their unique behaviors, respecting their boundaries, and appreciating their capacity for affection, we can deepen our connection with these enigmatic companions and continue to be fascinated by them for generations to come.

# This essay, roughly 480 words long, explores the various facets of our fascination with cats, from their duality and sensory prowess to their historical and cultural significance. It acknowledges both the positive and negative aspects of our "cat culture" and stresses the importance of responsible pet ownership. Feel free to request further exploration of specific points or a different perspective on the topic of cats. 
# """


# # TODO task for creating new user
# app = Flask(__name__)
# app.secret_key = "dasfar3qr21"
    
# @app.route('/',methods=["GET","POST"])
# def pinned_view():
#     # 99a74794-3194-44fc-8957-053ed2036fdc
#     # t=render_template("pinned_letter.html")
#     # print(t,type(t))
#     # form = WriteForm()
    
#     # TODO can try 2 ways
#     # this way of extending htmls 
#     # second using derive 2 render temoplats here and send for both sources from here on. (the problem is that base tempalte gets loaded 2 times)

#     value= "hey this worked! letter content"
    
#     return render_template("pinned_letter.html", value=value)

# # 
  


# if __name__ == "__main__":
#     app.run(debug=True,port=3000)