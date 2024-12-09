import React from 'react';
import { Text, View, Image, TouchableOpacity } from 'react-native';
import { StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from 'expo-router'; // Navigation hook

const logoImage = require('@/assets/images/logo.png');

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export default function Header({
  title = "Welcome to",
  subtitle = "Your All-In-One platform for smart construction and design solutions.",
}: HeaderProps) {
  const navigation = useNavigation();

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
        <Text style={styles.subtitle}>{subtitle}</Text>

        {/* Help Button */}
        <TouchableOpacity onPress={() => navigation.navigate('(aux)/help')}>
          <View style={styles.helpContainer}>
            <Ionicons style={styles.helpIcon} name="information-circle-outline" />
            <Text style={styles.helpText}>Help</Text>
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
  },
  logoContainer: {
    marginRight: 10,
  },
  logo: {
    width: 70,
    height: 70,
    borderRadius: 10,
  },
  welcomeContainer: {
    flex: 1,
  },
  titleWrapper: {
    flexDirection: 'row',
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
  helpIcon: {
    fontSize: 25,
    color: '#8ee7e4',
  },
  helpText: {
    fontSize: 10,
    color: '#fff',
    textTransform: 'uppercase',
    marginTop: 2,
  },
  helpContainer: {
    position: 'absolute',
    right: 10,
    bottom: 1,
    alignItems: 'center',
  },
});
