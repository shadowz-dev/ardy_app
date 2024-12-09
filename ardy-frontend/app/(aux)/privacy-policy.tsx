import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from 'expo-router';

export default function PrivacyPolicy() {
  const navigation = useNavigation();

  return (
    <ScrollView style={styles.container}>
      {/* Back Button */}
      <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
        <Ionicons name="arrow-back" size={24} color="#fff" />
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>

      {/* Header */}
      <Text style={styles.header}>Privacy Policy</Text>

      {/* Content */}
      <View style={styles.section}>
        <Text style={styles.paragraph}>
          Your privacy is important to us. This Privacy Policy explains how we collect, use, and share your information when you use our services.
        </Text>
        <Text style={styles.sectionTitle}>Information We Collect</Text>
        <Text style={styles.paragraph}>
          We collect personal information such as your name, email address, and usage data to improve our services.
        </Text>
        <Text style={styles.sectionTitle}>How We Use Your Information</Text>
        <Text style={styles.paragraph}>
          Your information is used to provide and improve our services, communicate with you, and comply with legal requirements.
        </Text>
        <Text style={styles.sectionTitle}>Your Choices</Text>
        <Text style={styles.paragraph}>
          You have the right to review, update, or delete your information. Please contact us at privacy@ardy.com for assistance.
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#2d363b', padding: 20 },
  backButton: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  backText: { color: '#fff', fontSize: 16, marginLeft: 5 },
  header: { fontSize: 26, fontWeight: 'bold', color: '#8ee7e4', marginBottom: 20, textAlign: 'center' },
  section: { marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#8ee7e4', marginTop: 10 },
  paragraph: { fontSize: 14, color: '#ccc', marginTop: 5, lineHeight: 20 },
});
