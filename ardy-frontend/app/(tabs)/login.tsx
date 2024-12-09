

import { SafeAreaView, ScrollView ,View, Text, TextInput, TouchableOpacity, StyleSheet, Dimensions, Image, Button, Alert } from 'react-native';
import React, { useState, useEffect } from 'react';
import { useSession } from '@/components/AuthContext';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Checkbox } from 'native-base';

const { width } = Dimensions.get('window');
const logoImage = require('@/assets/images/logo.png');

interface LoginScreenProps {
    defaultUser?: { email: string; password: string; role: string };
  }

export default function LoginScreen({ defaultUser }: LoginScreenProps) {
    const [email, setEmail] = useState(defaultUser?.email || '');
    const [password, setPassword] = useState(defaultUser?.password || '');
    const [isPasswordVisible, setPasswordVisible] = useState(false);
    const [rememberMe, setRememberMe] = useState(false);
    const [keepLoggedIn, setKeepLoggedIn] = useState(false);
    const { signIn, signOut} = useSession();

    useEffect(() => {
        // Load saved credentials
        loadRememberedCredentials();
      }, []);

    const togglePasswordVisibility = () => {
        setPasswordVisible(!isPasswordVisible);
      };
    
      const loadRememberedCredentials = async () => {
        const savedEmail = await AsyncStorage.getItem('rememberedEmail');
        const savedPassword = await AsyncStorage.getItem('rememberedPassword');
        const savedRememberMe = await AsyncStorage.getItem('rememberMe');
        
        if (savedRememberMe === 'true') {
          setEmail(savedEmail || '');
          setPassword(savedPassword || '');
          setRememberMe(true);
        }
      };
    
      const handleLogin = async () => {
        let roleToSignIn = 'Customer';
        // Handle your login logic here
        if (rememberMe) {
          await AsyncStorage.setItem('rememberedEmail', email);
          await AsyncStorage.setItem('rememberedPassword', password);
          await AsyncStorage.setItem('rememberMe', 'true');
        } else {
          await AsyncStorage.removeItem('rememberedEmail');
          await AsyncStorage.removeItem('rememberedPassword');
          await AsyncStorage.removeItem('rememberMe');
        }
        if (email === 'customer') {
            roleToSignIn = 'Customer';
            setEmail('customer');
            setPassword('customer123');
          } else if (email === 'service') {
            roleToSignIn = 'ServiceProvider';
            setEmail('service');
            setPassword('service123');
          } else {
            Alert.alert("Invalid Credentials", "Please enter valid credentials.");
            return;
          }
        
          // Simulate login
          await signIn(roleToSignIn);
          Alert.alert("Login Successful", `Welcome ${roleToSignIn}!`);
        
      };
  return (
    <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContainer}>
      {/* Logo Section */}
      <View style={styles.logoContainer}>
        <Image source={logoImage} style={styles.logo} />
      </View>

      {/* Title */}
      <Text style={styles.title}>Welcome Back</Text>
      <Text style={styles.subtitle}>Log in to your account</Text>

      {/* Email Input */}
      <View style={styles.inputContainer}>
        <Ionicons name="mail-outline" size={20} color="#8ee7e4" style={styles.inputIcon} />
        <TextInput
          placeholder="Email"
          placeholderTextColor="#aaa"
          value={email}
          onChangeText={setEmail}
          style={styles.input}
          keyboardType="email-address"
          autoCapitalize="none"
        />
      </View>

      {/* Password Input */}
      <View style={styles.inputContainer}>
        <Ionicons name="lock-closed-outline" size={20} color="#8ee7e4" style={styles.inputIcon} />
        <TextInput
          placeholder="Password"
          placeholderTextColor="#aaa"
          value={password}
          onChangeText={setPassword}
          style={styles.input}
          secureTextEntry={!isPasswordVisible}
        />
        <TouchableOpacity onPress={togglePasswordVisibility}>
          <Ionicons
            name={isPasswordVisible ? 'eye-outline' : 'eye-off-outline'}
            size={20}
            color="#aaa"
            style={styles.passwordIcon}
          />
        </TouchableOpacity>
      </View>
      {/* Checkboxes Section */}
      <View style={styles.checkboxContainer}>
  {/* Remember Me Checkbox */}
  <View style={styles.checkboxWrapper}>
    <Checkbox
    value="rememberMe" // Add a value here
    isChecked={rememberMe}
    onChange={() => setRememberMe(!rememberMe)}
    colorScheme="cyan"
    accessibilityLabel="Remember Me"
    >
    <Text style={styles.checkboxText}>Remember Me</Text>
    </Checkbox>
  </View>

  {/* Keep Me Logged In Checkbox */}
  <View style={styles.checkboxWrapper}>
    <Checkbox
    value="KeepLoggedIn" // Add a value here
    isChecked={keepLoggedIn}
    onChange={() => setKeepLoggedIn(!keepLoggedIn)}
    colorScheme="cyan"
    accessibilityLabel="Keep Me Logged In"
    >
    <Text style={styles.checkboxText}>Keep Me Logged In</Text>
    </Checkbox>
  </View>
</View>

      {/* Login Button */}
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>

      {/* Forgot Password */}
      <TouchableOpacity>
        <Text style={styles.forgotPassword}>Forgot Password?</Text>
      </TouchableOpacity>

      {/* Sign Up Link */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>Don't have an account?</Text>
        <TouchableOpacity>
          <Text style={styles.signupLink}> Sign Up</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
    </SafeAreaView>


  );
}
const styles = StyleSheet.create({
    container: {
    paddingTop: 20,
    flex: 1,
    backgroundColor: '#2d363b',
    justifyContent: 'center',
    paddingHorizontal: 20,
    },
    scrollContainer: {
        flexGrow: 1,
      },
    logoContainer: {
    alignItems: 'center',
    marginBottom: 30,
    },
    logo: {
    width: 100,
    height: 100,
    resizeMode: 'contain',
    borderRadius: 50,
    },
    title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#8ee7e4',
    textAlign: 'center',
    marginBottom: 10,
    },
    subtitle: {
      fontSize: 16,
      color: '#ccc',
      textAlign: 'center',
      marginBottom: 30,
    },
    inputContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      backgroundColor: '#3e444a',
      borderRadius: 8,
      padding: 10,
      marginBottom: 15,
    },
    input: {
      flex: 1,
      fontSize: 16,
      color: '#fff',
      marginLeft: 10,
    },
    inputIcon: {
      marginLeft: 5,
    },
    passwordIcon: {
      marginLeft: 5,
    },
    button: {
      backgroundColor: '#8ee7e4',
      borderRadius: 8,
      paddingVertical: 15,
      alignItems: 'center',
      marginTop: 10,
    },
    buttonText: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#2d363b',
    },
    forgotPassword: {
      color: '#8ee7e4',
      textAlign: 'center',
      marginVertical: 15,
      fontSize: 14,
    },
    footer: {
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 20,
    },
    footerText: {
      fontSize: 14,
      color: '#ccc',
    },
    signupLink: {
      fontSize: 14,
      fontWeight: 'bold',
      color: '#8ee7e4',
    },
    checkboxContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 8,
        alignItems: 'center',
      },
      checkboxWrapper: {
        flexDirection: 'row',
        alignItems: 'center',
      },
      checkboxText: {
        color: '#fff',
        marginLeft: 5,
        fontSize: 14,
      },
  });

