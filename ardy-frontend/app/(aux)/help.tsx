import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from 'expo-router';

const FAQ_DATA = [
  { 
    question: 'How do I reset my password?', 
    answer: 'To reset your password, go to the login screen and click on "Forgot Password". Follow the instructions sent to your email.' 
  },
  { 
    question: 'How can I contact support?', 
    answer: 'You can contact support via email at support@ardy.com or through the Contact Us form below.' 
  },
  { 
    question: 'What services do you offer?', 
    answer: 'We offer consultation, interior design, smart home services, and construction management solutions.' 
  },
  { 
    question: 'How do I track my projects?', 
    answer: 'You can track your projects by navigating to the "Projects" tab after logging in.' 
  },
];

export default function HelpScreen() {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const navigation = useNavigation();

  // Toggle FAQ answer visibility
  const toggleFAQ = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <ScrollView style={styles.container}>
      {/* Back Button */}
      <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
        <Ionicons name="arrow-back" size={24} color="#8ee7e4" />
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>
      
      {/* Header */}
      <Text style={styles.header}>Help & Support</Text>

      {/* FAQ Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
        {FAQ_DATA.map((item, index) => (
          <View key={index} style={styles.faqItem}>
            <TouchableOpacity onPress={() => toggleFAQ(index)}>
              <Text style={styles.faqQuestion}>
                {item.question}
              </Text>
            </TouchableOpacity>
            {expandedIndex === index && (
              <Text style={styles.faqAnswer}>{item.answer}</Text>
            )}
          </View>
        ))}
      </View>

      {/* Email Us Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Email Us</Text>
        <TouchableOpacity style={styles.actionButton} onPress={() => console.log('Email Triggered')}>
          <Ionicons name="mail-outline" size={24} color="#8ee7e4" />
          <Text style={styles.actionText}>Send us an Email</Text>
        </TouchableOpacity>
      </View>

      {/* Chat With Us Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Chat With Us</Text>
        <TouchableOpacity style={styles.actionButton} onPress={() => navigation.navigate('(aux)/helpdesk-chat')}>
          <Ionicons name="chatbubbles-outline" size={24} color="#8ee7e4" />
          <Text style={styles.actionText}>Chat with Support</Text>
        </TouchableOpacity>
      </View>

      {/* Contact Us Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact Us</Text>
        <View style={styles.contactInfo}>
          <Text style={styles.contactText}>Email: support@ardy.com</Text>
          <Text style={styles.contactText}>Phone: +1 (234) 567-890</Text>
          <Text style={styles.contactText}>Working Hours: Mon-Fri, 9:00 AM - 5:00 PM</Text>
        </View>
      </View>

      {/* Navigation Buttons for Privacy Policy and Terms */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Legal</Text>
        <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('(aux)/privacy-policy')}>
          <Ionicons name="document-text-outline" size={20} color="#fff" />
          <Text style={styles.buttonText}>Privacy Policy</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('(aux)/terms-of-service')}>
          <Ionicons name="document-text-outline" size={20} color="#fff" />
          <Text style={styles.buttonText}>Terms of Service</Text>
        </TouchableOpacity>
        </View>
      </View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2d363b',
    padding: 20,
  },
  header: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#8ee7e4',
    marginBottom: 20,
    textAlign: 'center',
  },
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 15,
  },
  faqItem: {
    marginBottom: 10,
    backgroundColor: '#3e444a',
    borderRadius: 8,
    padding: 10,
    elevation: 2,
  },
  faqQuestion: {
    fontSize: 16,
    fontWeight: '600',
    color: '#8ee7e4',
  },
  faqAnswer: {
    fontSize: 14,
    color: '#ccc',
    marginTop: 5,
  },
  contactInfo: {
    backgroundColor: '#3e444a',
    borderRadius: 8,
    padding: 15,
    elevation: 2,
  },
  contactText: {
    fontSize: 16,
    color: '#ccc',
    marginBottom: 8,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  backText: {
    color: '#fff',
    fontSize: 16,
    marginLeft: 5,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#3e444a',
    padding: 15,
    borderRadius: 8,
    elevation: 2,
  },
  actionText: {
    color: '#fff',
    fontSize: 16,
    marginLeft: 10,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#3e444a',
    padding: 15,
    borderRadius: 8,
    width: '48%', // Ensures equal spacing for 2 buttons
  },
  buttonText: {
    color: '#8ee7e4',
    fontSize: 16,
    marginLeft: 10,
  },
});
