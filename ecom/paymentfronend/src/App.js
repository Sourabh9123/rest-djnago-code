import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import useRazorpay from "react-razorpay";

import MyComponent from './GoogleLogin2';
import GoogleLogin from "react-google-login";
import { useEffect } from 'react';
import  { jwtDecode } from "jwt-decode"


function App() {
  
  const [Razorpay] = useRazorpay();
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5OTM4OTA5LCJpYXQiOjE2OTk4ODQ5MDksImp0aSI6Ijk2MjAyMTliNjE2NjQ1NzA5OTNiMjc5Njg3OGI1ZGY3IiwidXNlcl9pZCI6IjE4ZTQ5ZjNhLTM4Y2ItNDMyZi1hNTcxLTIwOTdmNzY1OTE1NyJ9.bWWeseO3Hz1zNILFs6QDHbO9bnScjhr6q7guXNHvcqM";
  const data = {
    firstName: 'Fred',
    lastName: 'Flintstone'
  };
  
  // Define the headers with the Bearer token
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json' // Set the content type if needed
  };
  
  const complete_payment = (razorpay_payment_id,razorpay_order_id,razorpay_signature,current_amount) => {
    axios.post('http://127.0.0.1:8000/api/cart/order/transaction/', {
      
      "payment_id":razorpay_payment_id,
      "order_id": razorpay_order_id, 
      "signature": razorpay_signature,
      "amount" :current_amount
    
    })
      .then((response) => {
        console.log(response.data);
        console.log("function inside fun ")
        console.log(current_amount, "current amt")
      }) 
      .catch(error => {
        console.log(error);
      });
  };

  

  // Make the POST request using an arrow function
  const postData = () => {
    axios.post('http://127.0.0.1:8000/api/cart/order/', data, { headers: headers })
      .then(response => {
        console.log(response.data);
        console.log(response.data.order.amount)
       const order_id = response.data.payment.id
       const current_amount = response.data.order.amount
   

       const options = {
        key: "rzp_test_DqyEDw9vF6Y4kA", // Enter the Key ID generated from the Dashboard
        
        name: "Acme Corp",
        description: "Test Transaction",
        image: "https://example.com/your_logo",
        order_id: order_id, //This is a sample Order ID. Pass the `id` obtained in the response of createOrder().
        handler: function (response) {
     
         
          complete_payment(response.razorpay_payment_id,response.razorpay_order_id ,response.razorpay_signature, current_amount)
          
          
        },
        prefill: {
          name: "Sourabh Das",
          email: "skd@gmail.com",
          contact: "8444869123",
        },
        notes: {
          address: "Razorpay Corporate Office",
        },
        theme: {
          color: "#3399cc",
        },
      };
    
      const rzp1 = new Razorpay(options);
    
      rzp1.on("payment.failed", function (response) {
        alert(response.error.code);
        alert(response.error.description);
        alert(response.error.source);
        alert(response.error.step);
        alert(response.error.reason);
        alert(response.error.metadata.order_id);
        alert(response.error.metadata.payment_id);
      });
    
      rzp1.open();


      })
      .catch(error => {
        console.log(error);
      });
  };
 
  


const googleClientId = "770476220582-4sbpgt50vrhv1fr1ufv3t8hhhnvh7ulr.apps.googleusercontent.com"
const drfClientId ="uNzh40qPSQpaS6MUqXaVGXKQ3OoLOQ6fyGB0HZUb"
const drfClientSecret = "pbkdf2_sha256$600000$KDa36wZPWo8qasGhoDXq3X$K5TcFdXpV0TwJ6x0XpNgITw9RUnjpjFUeevHVxjgrmA="
const baseURL = "http://localhost:8000";



  const handleGoogleLogin = (response) => {
    axios
      .post(`${baseURL}/auth/convert-token`, {
        token: response.accessToken,
        backend: "google-oauth2",
        grant_type: "convert_token",
        client_id: drfClientId,
        client_secret: drfClientSecret,
      })
      .then((res) => {
        const { access_token, refresh_token } = res.data;
        console.log(res.data,"data-------------------------")
        console.log({ access_token, refresh_token });
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
      })
      .catch((err) => {
        console.log("Error Google login", err);
      });
  };





// useEffect(()=>{


//   google.accounts.id.initialize({
//     client_id: "865719858663-gg9elga73ae9lb5sivo10ojspnd1lktb.apps.googleusercontent.com",
//     callback: handelCallBackResponse
//   });

  

//   google.accounts.id.renderButton(
//     document.getElementById("signInDiv"),
//     {
//       theme : "outline", size :"large"
//     }
//   )
// },[])



function handelCallBackResponse(response){
  console.log(response.credential)
  console.log(response)
  const decode_data = jwtDecode(response.credential)
  console.log(decode_data)
  const data_user =  response
  

  fetch('http://127.0.0.1:8000/api/account/google/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({decode_data}),
    })
      .then((response) => {
        if (response.status === 200) {
          // Handle successful login, e.g., redirect the user or update the UI
          console.log('Google login successful');
          console.log(response.token)
          
        } else {
          // Handle login failure or errors
          console.error('Google login failed');
        }
      })
      .catch((error) => {
        console.error('Error while logging in:', error);
      });
  

}


useEffect(() => {
  /* global google */
  if (typeof google !== 'undefined') {
    google.accounts.id.initialize({
      client_id: '865719858663-gg9elga73ae9lb5sivo10ojspnd1lktb.apps.googleusercontent.com', // Replace with your client ID
      callback: handelCallBackResponse
    });

    google.accounts.id.renderButton(
      document.getElementById('signInDiv'),
      {
        theme: 'outline',
        size: 'large'
      }
    );
  }
}, []);




  return (
    <>
    <div className='App'>
      


    <div id="signInDiv">googleLogin</div>

      
    </div>
{/* 
<div className="App">
      <GoogleLogin
        clientId={googleClientId}
        buttonText="LOGIN WITH GOOGLE"
        onSuccess={(response) => handleGoogleLogin(response)}
        render={(renderProps) => (
          <button
            onClick={renderProps.onClick}
            disabled={renderProps.disabled}
            type="button"
            className="login-with-google-btn"
          >
            Sign in with Google
          </button>
        )}
        onFailure={(err) => console.log("Google Login failed", err)}
      />
    </div> */}


  
      <button type="button" onClick={postData} className="btn btn-primary mx-2">Payment</button> 
      
      {/* <div className="btn  mx-2">
      <GoogleLoginButton />
      </div> */}

      
      {/* <div className="btn  mx-2">
      <MyComponent />
      </div> */}


{/*       
      <button type="button" onClick={GoogleLoginButton} className="btn  mx-2">Google Login</button> */}
      
 
    </>
  );
}

export default App;







// cl = "865719858663-gg9elga73ae9lb5sivo10ojspnd1lktb.apps.googleusercontent.com"
// cs= "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"


