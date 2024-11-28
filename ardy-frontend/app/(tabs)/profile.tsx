import { Text, View, StyleSheet, Button } from 'react-native';
import React from 'react';
import { useSession } from '@/components/AuthContext';

export default function ProfileScreen() {
    const { signIn, signOut} = useSession();
  return (
    <View style={styles.container}>
      <Text style={styles.text}>My Profile</Text>
      <Button title="Logout" onPress={signOut} />
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
});
