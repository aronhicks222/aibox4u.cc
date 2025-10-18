import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { useToast } from '../hooks/use-toast';
import { submissionsAPI, categoriesAPI } from '../api';

const SubmitTool = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [categories, setCategories] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    longDescription: '',
    category: '',
    pricing: '',
    url: '',
    imageUrl: '',
    tags: '',
    submitterEmail: ''
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories((response.data.categories || []).filter(c => c !== 'All'));
    } catch (err) {
      console.error('Failed to load categories', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await submissionsAPI.create(formData);
      toast({
        title: "Tool Submitted Successfully!",
        description: "Thank you! We'll review your submission and add it to the directory soon.",
      });
      setTimeout(() => navigate('/'), 2000);
    } catch (err) {
      toast({
        title: "Submission Failed",
        description: err.response?.data?.detail || "An error occurred. Please try again.",
        variant: "destructive"
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-br from-purple-600 to-pink-500 text-white py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <Button variant="ghost" onClick={() => navigate('/')} className="text-white hover:bg-white/20 mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          <h1 className="text-4xl font-bold mb-2">Submit Your AI Tool</h1>
          <p className="text-lg opacity-90">Share your amazing AI tool with our community</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <Card>
          <CardHeader>
            <CardTitle>Tool Information</CardTitle>
            <CardDescription>Fill in the details about your AI tool. All fields are required.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <Label htmlFor="name">Tool Name *</Label>
                <Input 
                  id="name"
                  name="name"
                  placeholder="e.g., ChatGPT, Midjourney"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="description">Short Description *</Label>
                <Textarea 
                  id="description"
                  name="description"
                  placeholder="Brief description (max 200 characters)"
                  value={formData.description}
                  onChange={handleChange}
                  required
                  maxLength={200}
                  rows={3}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="longDescription">Full Description *</Label>
                <Textarea 
                  id="longDescription"
                  name="longDescription"
                  placeholder="Detailed description of your tool and its features"
                  value={formData.longDescription}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="mt-1"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="category">Category *</Label>
                  <Select 
                    value={formData.category} 
                    onValueChange={(value) => setFormData({...formData, category: value})}
                    required
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map(cat => (
                        <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="pricing">Pricing *</Label>
                  <Select 
                    value={formData.pricing} 
                    onValueChange={(value) => setFormData({...formData, pricing: value})}
                    required
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select pricing" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Free">Free</SelectItem>
                      <SelectItem value="Paid">Paid</SelectItem>
                      <SelectItem value="Freemium">Freemium</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="url">Website URL *</Label>
                <Input 
                  id="url"
                  name="url"
                  type="url"
                  placeholder="https://yourtool.com"
                  value={formData.url}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="imageUrl">Screenshot/Image URL *</Label>
                <Input 
                  id="imageUrl"
                  name="imageUrl"
                  type="url"
                  placeholder="https://example.com/image.jpg"
                  value={formData.imageUrl}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="tags">Tags (comma-separated) *</Label>
                <Input 
                  id="tags"
                  name="tags"
                  placeholder="#AI, #Productivity, #Automation"
                  value={formData.tags}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="submitterEmail">Your Email *</Label>
                <Input 
                  id="submitterEmail"
                  name="submitterEmail"
                  type="email"
                  placeholder="your@email.com"
                  value={formData.submitterEmail}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div className="flex gap-4 pt-4">
                <Button type="submit" className="bg-pink-600 hover:bg-pink-700 text-white flex-1">
                  Submit Tool
                </Button>
                <Button type="button" variant="outline" onClick={() => navigate('/')} className="flex-1">
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SubmitTool;
