import React from 'react';
import { Text, View, Image } from 'react-native';
import { StyleSheet } from 'react-native';

const logoImage = require('@/assets/images/logo.png');

interface HeaderProps {
  title?: string; // Custom title
  subtitle?: string; // Custom subtitle
}

export default function Header({ title = "Welcome to", subtitle = "Your All-In-One platform for smart construction and design solutions." }: HeaderProps) {
  return (
    <View style={styles.header}>
      <View style={styles.logoContainer}>
        <Image source={logoImage} style={styles.logo} />
      </View>
      <View style={styles.welcomeContainer}>
        <View style={styles.titleWrapper}>
          <Text style={styles.title}>Ardy! </Text>
          <Text style={styles.titleAccent}>{title}</Text>
        </View>
        <Text style={styles.subtitle}>
          {subtitle}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row', // Align logo and welcome container in a row
    alignItems: 'center', // Vertically align content
    padding: 10,
  },
  logoContainer: {
    marginRight: 10, // Add space between the logo and welcome text
  },
  logo: {
    width: 70,
    height: 70,
    borderRadius: 10,
  },
  welcomeContainer: {
    flex: 1, // Take remaining space
  },
  titleWrapper: {
    flexDirection: 'row', // Align title and titleAccent horizontally
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#8ee7e4',
  },
  titleAccent: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
  },
});
