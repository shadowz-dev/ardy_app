import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from 'expo-router';

export default function TermsOfService() {
  const navigation = useNavigation();

  return (
    <ScrollView style={styles.container}>
      {/* Back Button */}
      <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
        <Ionicons name="arrow-back" size={24} color="#fff" />
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>

      {/* Header */}
      <Text style={styles.header}>Terms of Service</Text>

      {/* Content */}
      <View style={styles.section}>
        <Text style={styles.paragraph}>
          By using our services, you agree to these terms. Please read them carefully.
        </Text>
        <Text style={styles.sectionTitle}>Use of Services</Text>
        <Text style={styles.paragraph}>
          You may use our services only as permitted by law. Unauthorized use is strictly prohibited.
        </Text>
        <Text style={styles.sectionTitle}>Your Responsibilities</Text>
        <Text style={styles.paragraph}>
          You are responsible for maintaining the confidentiality of your account and ensuring lawful use of our services.
        </Text>
        <Text style={styles.sectionTitle}>Termination</Text>
        <Text style={styles.paragraph}>
          We may terminate or suspend your access to our services if you violate these terms.
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
