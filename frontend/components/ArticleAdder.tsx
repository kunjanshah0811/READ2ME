import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';

export default function ArticleAdder() {
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');

  const handleAddUrl = async () => {
    try {
      const response = await fetch('http://localhost:7777/v1/url/full', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, tts_engine: 'edge' }),
      });
      if (!response.ok) throw new Error('Failed to add URL');
      setUrl('');
      alert('URL added successfully');
    } catch (error) {
      console.error('Error adding URL:', error);
      alert('Failed to add URL');
    }
  };

  const handleAddText = async () => {
    try {
      const response = await fetch('http://localhost:7777/v1/text/full', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, tts_engine: 'edge' }),
      });
      if (!response.ok) throw new Error('Failed to add text');
      setText('');
      alert('Text added successfully');
    } catch (error) {
      console.error('Error adding text:', error);
      alert('Failed to add text');
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Add Single Article</h2>
      <div className="flex space-x-2">
        <Input
          type="text"
          placeholder="Article URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <Button onClick={handleAddUrl}>Add URL</Button>
      </div>
      <div className="space-y-2">
        <Textarea
          placeholder="Article text"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <Button onClick={handleAddText}>Add Text</Button>
      </div>
    </div>
  );
}