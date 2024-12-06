

import { Text, View, StyleSheet, Button } from 'react-native';
import React from 'react';
import { useSession } from '@/components/AuthContext';
export default function LoginScreen() {
    const { signIn, signOut} = useSession();
  return (
    <View style={styles.container}>
        <Text style={styles.text}>Login screen</Text>
      <Text style={styles.text}>This is the login screen</Text>
      <Button title="Login as Customer" onPress={() => signIn('Customer')} />
      <Button title="Login as ServiceProvider" onPress={() => signIn('ServiceProvider')} />
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2d363b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: '#fff',
  },
  buttonTitle: {
    marginBottom: 10,
    marginTop: 10,
  }
});

