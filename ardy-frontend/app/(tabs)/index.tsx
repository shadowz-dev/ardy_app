import { Text, View, StyleSheet } from 'react-native';
import { Link } from 'expo-router';
import { Image } from 'expo-image';

const logoImage = require('@/assets/images/logo.png');
export default function Index() {
  return (
    <View style={styles.container}>
      <Image source={logoImage} style={styles.image} />
      <View style={{flexDirection: 'row'}}>
        <Text style={styles.title}>Welcome to</Text>
        <Text style={styles.title1}> Ardy !</Text>
      </View>
      <View style={{flexDirection: 'row'}}>
        <Text style={styles.subtitle}>All-In-One </Text>
        <Text style={styles.subtitle1}>patform</Text>
      </View>
      <Text style={styles.subtitle}>smart construction and design solutions.</Text>
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
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
  },
  title1: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#8ee7e4',
    marginBottom: 20,
    shadowOpacity: 0.8,
  },
  subtitle: {
    fontSize: 14,
    textAlign: 'center',
    color: '#fff',
  },
  subtitle1: {
    fontSize: 14,
    textAlign: 'right',
    color: '#8ee7e4',
  },
  button: {
    fontSize: 20,
    textDecorationLine: 'underline',
    color: 'green',
  },
  image: {
    width: 150,
    height: 150,
    marginBottom: 20,
    borderRadius: 50,
  },
});