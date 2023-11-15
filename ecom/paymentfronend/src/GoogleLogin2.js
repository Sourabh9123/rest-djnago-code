import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';

class MyComponent extends Component {
  onGoogleLogin = (accessToken) => {
     console.log(accessToken,"this is token ------------------------------------------")
    // Send the Google access token to your Django backend
    fetch('http://127.0.0.1:8000/api/account/google/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ access_token: accessToken }),
    })
      .then((response) => {
        if (response.status === 200) {
          // Handle successful login, e.g., redirect the user or update the UI
          console.log('Google login successful');
        } else {
          // Handle login failure or errors
          console.error('Google login failed');
        }
      })
      .catch((error) => {
        console.error('Error while logging in:', error);
      });
  };

  render() {
    return (
      <div>
        <GoogleLogin
          // clientId="46446715863-rlfm27iovjurakn4kagcnrmscc2me86n.apps.googleusercontent.com"
          clientId= "770476220582-4sbpgt50vrhv1fr1ufv3t8hhhnvh7ulr.apps.googleusercontent.com"
          buttonText="Login with Google"
          onSuccess={this.onGoogleLogin}
          onFailure={this.onGoogleLogin}
          cookiePolicy={'single_host_origin'}
          
        />
      </div>
    );
  }
}

export default MyComponent;
