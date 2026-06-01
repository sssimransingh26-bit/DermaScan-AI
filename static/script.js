function previewImage(event)
{
    const file=event.target.files[0];
    if(!file) return;

    const preview=document.getElementById('preview');
    const uploadPrompt=document.getElementById('uploadPrompt');
    document.getElementById('uploadBox').classList.add('has-image');
    preview.src=URL.createObjectURL(file);
    preview.style.display='block';//display:none so display:block makes it visible
    uploadPrompt.style.display='none';//hides upload text
}


async function uploadImage() 
{
    const file=document.getElementById('imageInput').files[0];
    if(!file)
    {
        alert('Please select an image first');
        return;
    }

    document.getElementById('loader').style.display='block';
    document.getElementById('resultBox').style.display='none';//if previos prediction exist it hides it while processing new image

    const formData=new FormData();
    formData.append('file',file);

    try{
        const response=await fetch('/predict',{
            method:'POST',
            body:formData
        });

        const data=await response.json();

        //checking for quality error
        if(data.error)
        {
            document.getElementById('loader').style.display='none';
            alert(data.error);
            return;
        }

        //hide loader after success
        document.getElementById('loader').style.display='none';

        //result
        document.getElementById('conditionText').innerText=data.condition;
        document.getElementById('confidenceLabel').innerText = `Confidence: ${data.confidence}%`;
        document.getElementById('confidenceFill').style.width = `${data.confidence}%`;

        //description and consult
        document.getElementById('descriptionText').innerText = data.description;
        document.getElementById('consultText').innerText = data.consult_when;

        //severity
        const badge=document.getElementById('severityBadge');
        badge.innerText=`Severity: ${data.severity}`;
        badge.className=`severity-badge severity-${data.severity.toLowerCase()}`;

        //symptoms
        const symptomsList=document.getElementById('symptomsList');
        symptomsList.innerHTML=data.symptoms.map(s => `<li>${s}</li>`).join('');

        //precautions
        const precautionsList=document.getElementById('precautionsList');
        precautionsList.innerHTML=data.precautions.map(p => `<li>${p}</li>`).join('');

        //result box
        document.getElementById('placeholderBox').style.display = 'none';
        document.getElementById('resultBox').style.display = 'block';
    }
    catch (error){
        document.getElementById('loader').style.display='none';
        alert('something went wrong. Please try again');
    }
    
}

function toggleMode()
{
    const body=document.body;
    const btn=document.querySelector('.toggle-btn');

    body.classList.toggle('light');

    if(body.classList.contains('light'))
    {
        btn.innerText='Dark Mode';
    }
    else{
        btn.innerText='Light Mode';
    }
}