import streamlit as st

def show():
    st.header("🏠 Introduction")
    st.write("What is the need for a classification app?") 

    # st.write("{text from report}")

    tab1, tab2= st.tabs(["Intro Context and Objective", 
                                "Intro ResNet50"])

    # :material/subdirectory_arrow_right

    with tab1:
        st.subheader("Context of the project")
        st.markdown("""
        > While COVID-19 has **shifted from pandemic to endemic status** in 2025, respiratory infections **remain** a persistent health **challenge worldwide**.  
        > **Chest X-ray** (CXR) imaging continues to be widely **available**, relatively **inexpensive**, and **faster** to perform than many other diagnostic methods.    
                           
        :green-badge[- This makes it a **practical tool** for **screening** and **triage** in both high- and low-resource settings.]    
        :green-badge[- Accurate CXR classification not only **supports the identification** of **COVID-19**  
                      but also aids in detecting **other non-COVID lung infections**, such as viral pneumonia.]  
        :green-badge[- Thereby, it helps to **manage patient flow**,  
                      **support clinical decision-making**,  
                    **reduce the overall burden** on **healthcare systems**.]
                    
        > While molecular tests like **RT-PCR** remain the **gold standard** for COVID-19 diagnosis, they are **not always accessible** or **timely**, especially in resource-limited regions or during surges in patient
        > numbers. 
                    
        ➤ Chest X-rays offer a **complementary approach**:   
        :green-badge[- they are **quick to acquire**,]  
        :green-badge[- can be **performed at the bedside**,]    
        :green-badge[- and are **already integrated** into routine clinical workflows.]  
                    
        > However, the accuracy of PCR tests is generally higher than that of X-ray-based classification. Distinguishing COVID-19 from  
        > other lung conditions—such as viral pneumonia or bacterial infections solely based on CXR images is challenging for both  
        > clinicians and current AI tools.  
        > This challenge is further compounded by variations in image quality, patient demographics, and the potential for overlapping  
        > radiological features between diseases.  
                    """, unsafe_allow_html=True) 
        
        st.markdown("""
        Our **project aims** to **develop** a **well-performing deep learning model** capable of **accurately distinguishing 4 classes**:  
        :green-badge[(1) COVID-19 positive,]    
        :green-badge[(2) viral pneumonia,]  
        :green-badge[(3) unremarkable / healthy and]    
        :green-badge[(4) lung opacity.]  
        
        For this purpose, a deep learning model will be set-up, trained (**_Transfer Learning_**), and evaluated on a test dataset. 
                    
                    """)

        
        
                 

    # with tab2:
    #     st.subheader("Objectives for the model development")
    #     # st.subheader("Main objective")
    #     # with st.expander("Main objective"):
    #     st.markdown("""
    #     **_Training a deep learning model_**
    #     - distinguish X-ray image from COVID patients from those with viral pneumonia or
    #     lung opacity and those with a lung disease (**multi-class classification**)  
        

    #     """)
    
        # st.divider()

    with tab2:
        st.header("Introduction to CNN ResNet 50")
        st.markdown(""" 
        We used the ResNet50 architecture as the **backbone of our classification model**. ResNet50 is a deep convolutional neural network with **50 layers**,
        originally introduced by He et al. in 2015. It is well known for its **residual connections**, which allow the neural network to learn identity mappings
        via **skip connections**, and helps by doing so **mitigating the vanishing gradient problem**. The ResNet50 framework allows gradients to flow more directly
        across layers, so a training of very deep architectures is enabled. ResNet50 has been **pretrained on the ImageNet dataset**, making it a strong candidate
        for transfer learning tasks in medical imaging, where annotated data is often limited.
        Although the name "ResNet50" refers to 50 convolutional and fully connected layers with trainable parameters, the **actual model** in Keras consists of
        more than **170 layers**. This is because operations such as activations, batch normalizations, and residual additions are represented as individual
        layers. For fine-tuning purposes, we typically focus on trainable convolutional layers rather than counting all layers indiscriminately.
        <br> 
        """, unsafe_allow_html=True)

        with st.popover("INFO: ResNet50 Composition", width="stretch"):
            st.image("/workspaces/may25_bds_covid19/streamlit/app/static_files/eda_files/resnet.png", width="stretch")
            st.caption("taken from https://blog.aiensured.com/resnet50/")


        with st.expander("INFO ‘vanishing gradient problem’"):
            st.markdown('''
            In machine learning, the vanishing gradient problem is the problem of greatly diverging gradient magnitudes 
            between earlier and later layers encountered when training neural networks with backpropagation. In such methods 
            neural network weights are updated proportional to their partial derivative of the loss function. As the number of 
            forward propagation steps in a network increases, for instance due to greater network depth, the gradients of 
            earlier weights are calculated with increasingly many multiplications. These multiplications shrink the gradient 
            magnitude. Consequently, the gradients of earlier weights will be exponentially smaller than the gradients of later 
            weights. This difference in gradient magnitude might introduce instability in the training process, slow it, or 
            halt it entirely. For instance, consider the hyperbolic tangent activation function. The gradients of this function 
            are in range [−1,1]. The product of repeated multiplication with such gradients decreases exponentially. The 
            inverse problem, when weight gradients at earlier layers get exponentially larger, is called the exploding gradient 
            problem.
            <a href="https://en.wikipedia.org/wiki/Vanishing_gradient_problem">Source</a>
            ''', unsafe_allow_html=True)

        # st.write("ADD AN IMAGE HOW RESNET IS COMPOSED!!!!")

# In our setup, the convolutional base of ResNet50 was initially frozen to retain its learned feature representations. A custom classification head
#        consisting of global average pooling, dropout, and one dense layer was appended to adapt the model to our four-class prediction task: COVID,
#        LUNG_OPACITY, NORMAL, and VIRAL_PNEUMONIA.